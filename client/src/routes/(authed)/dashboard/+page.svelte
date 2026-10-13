<script>
	import { goto } from '$app/navigation';
	import { baseURL, selectedBookId, selectedLanguage, wordGoal } from '$lib/state.svelte.js';
	import { AlertCircle, Book, BookOpen, Library, RotateCcw, Upload } from 'lucide-svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import LanguageSelector from '$lib/components/LanguageSelector.svelte';
	import WordGoalProgress from '$lib/components/WordGoalProgress.svelte';
	import WordGoalModal from '$lib/components/WordGoalModal.svelte';
	import BookCard from '$lib/components/BookCard.svelte';
	import DeleteBookModal from '$lib/components/DeleteBookModal.svelte';

	let continueReading = $state([]);
	let library = $state([]);
	let isLoading = $state(true);
	let error = $state(null);
	let showLanguageModal = $state(false);
	let showGoalModal = $state(false);
	let showDeleteModal = $state(false);
	let bookToDelete = $state(null);
	let wordsReadToday = $state(0);

	function requestDelete(book) {
		bookToDelete = book;
		showDeleteModal = true;
	}

	async function markUnread(bookId) {
		try {
			const response = await fetch(`${baseURL}/app/books/mark-unread`, {
				method: 'POST',
				credentials: 'include',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ book_id: bookId })
			});
			if (!response.ok) {
				throw new Error('Failed to mark book as unread');
			}
			await fetchBooks();
		} catch (err) {
			console.error('Error marking book as unread:', err);
		}
	}

	function downloadBook(bookId) {
		// Navigate to the endpoint so the browser follows the server's
		// Content-Disposition header and uses the original filename.
		const link = document.createElement('a');
		link.href = `${baseURL}/app/books/${bookId}/download`;
		document.body.appendChild(link);
		link.click();
		link.remove();
	}

	async function fetchBooks() {
		isLoading = true;
		error = null;
		try {
			const response = await fetch(
				`${baseURL}/app/dashboard/books?language=${selectedLanguage.value}`,
				{
					credentials: 'include'
				}
			);
			if (!response.ok) {
				throw new Error('Failed to fetch books');
			}
			const data = await response.json();

			console.log('Fetched books:', data);

			continueReading = data.continue_reading || [];
			library = data.library || [];
		} catch (err) {
			error = err.message;
			console.error('Error fetching books:', err);
		} finally {
			isLoading = false;
		}

		try {
			const logResponse = await fetch(`${baseURL}/app/reading-log/today`, {
				credentials: 'include'
			});
			if (logResponse.ok) {
				const logData = await logResponse.json();
				wordsReadToday = logData.word_count ?? 0;
				wordGoal.value = logData.word_goal ?? 0;
			}
		} catch (err) {
			console.error('Error fetching reading log:', err);
		}
	}

	$effect(() => {
		if (selectedLanguage.value) {
			fetchBooks();
		} else {
			showLanguageModal = true;
		}
	});

	function openBook(id) {
		selectedBookId.value = id;
		goto('/read');
	}
</script>

<svelte:head>
	<title>Dashboard — readablock</title>
</svelte:head>

<div class="min-h-screen bg-base-100">
	<PageHeader title="Dashboard" subtitle="Continue your reading journey or explore your library." />

	<div class="max-w-6xl mx-auto px-8 py-10">
		{#if isLoading}
			<div class="flex justify-center items-center h-64">
				<span class="loading loading-spinner loading-lg text-primary"></span>
			</div>
		{:else if error}
			<div role="alert" class="alert alert-error">
				<AlertCircle class="h-6 w-6 shrink-0" />
				<span>{error}</span>
				<button class="btn btn-sm btn-ghost gap-1" onclick={fetchBooks}>
					<RotateCcw class="h-4 w-4" /> Retry
				</button>
			</div>
		{:else if continueReading.length === 0 && library.length === 0}
			<!-- Empty state -->
			<div class="hero min-h-[60vh]">
				<div class="hero-content text-center flex-col">
					<Library class="h-20 w-20 text-base-content/20" />
					<div>
						<h2 class="text-2xl font-bold">No books yet</h2>
						<p class="py-4 text-base-content/60 max-w-sm">
							Start your reading journey by uploading your first book.
						</p>
						<a href="/upload" class="btn btn-primary btn-lg gap-2">
							<Upload class="h-5 w-5" /> Upload a book
						</a>
					</div>
				</div>
			</div>
		{:else}
			<!-- Daily word goal -->
			<section class="mb-12">
				<div class="card bg-base-200 border border-base-300 p-4">
					<WordGoalProgress
						wordCount={wordsReadToday}
						wordGoal={wordGoal.value ?? 0}
						onSetGoal={() => (showGoalModal = true)}
					/>
				</div>
			</section>

			<!-- Continue Reading -->
			{#if continueReading.length > 0}
				<section class="mb-12">
					<div class="flex items-center gap-3 mb-6">
						<BookOpen class="h-5 w-5 text-primary" />
						<h2 class="text-xl font-bold text-base-content">Continue Reading</h2>
						<div class="badge badge-primary badge-soft">{continueReading.length}</div>
					</div>
					<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
						{#each continueReading as book (book.id)}
							<BookCard {book} onopen={openBook} onunread={markUnread} ondownload={downloadBook} ondelete={requestDelete} />
						{/each}
					</div>
				</section>

				<div class="divider"></div>
			{/if}

			<!-- Library -->
			{#if library.length > 0}
				<section>
					<div class="flex items-center gap-3 mb-6">
						<Book class="h-5 w-5 text-secondary" />
						<h2 class="text-xl font-bold text-base-content">Your Library</h2>
						<div class="badge badge-secondary badge-soft">{library.length}</div>
					</div>
					<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
						{#each library as book (book.id)}
							<BookCard {book} onopen={openBook} onunread={markUnread} ondownload={downloadBook} ondelete={requestDelete} />
						{/each}
					</div>
				</section>
			{/if}
		{/if}
	</div>
</div>

<LanguageSelector bind:open={showLanguageModal} />
<WordGoalModal bind:open={showGoalModal} onSetGoal={(goal) => (wordGoal.value = goal)} />
<DeleteBookModal bind:open={showDeleteModal} book={bookToDelete} onDeleted={fetchBooks} />
