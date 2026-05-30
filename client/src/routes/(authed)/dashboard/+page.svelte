<script>
	import { goto } from '$app/navigation';
	import { baseURL, selectedBookId, selectedLanguage } from '$lib/state.svelte.js';
	import { AlertCircle, Book, BookOpen, Library, RotateCcw, Upload } from 'lucide-svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import LanguageSelector from '$lib/components/LanguageSelector.svelte';

	let continueReading = $state([]);
	let library = $state([]);
	let isLoading = $state(true);
	let error = $state(null);
	let showLanguageModal = $state(false);

	async function fetchBooks() {
		isLoading = true;
		error = null;
		try {
			const response = await fetch(`${baseURL}/app/dashboard/books?language=${selectedLanguage.value}`, {
				credentials: 'include'
			});
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
			<!-- Continue Reading -->
			{#if continueReading.length > 0}
				<section class="mb-12">
					<div class="flex items-center gap-3 mb-6">
						<BookOpen class="h-5 w-5 text-primary" />
						<h2 class="text-xl font-bold text-base-content">Continue Reading</h2>
						<div class="badge badge-primary badge-soft">{continueReading.length}</div>
					</div>
					<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
						{#each continueReading as book}
							<button
								onclick={() => openBook(book.id)}
								class="card w-full bg-base-200 border border-base-300 hover:border-primary hover:shadow-lg transition-all duration-200 cursor-pointer text-left p-4"
							>
								<div class="flex flex-col gap-4">
									<div
										class="aspect-[3/4] w-full bg-base-300 rounded-lg flex items-center justify-center"
									>
										<BookOpen class="h-12 w-12 text-primary" />
									</div>
									<div class="flex flex-col gap-3">
										<div class="flex flex-row items-center gap-3">
											<progress
												class="progress progress-primary flex-1 h-1.5"
												value={book.sentence_last_read}
												max="100"
											></progress>
											<span class="text-xs font-bold text-primary">{book.sentence_last_read}%</span>
										</div>
										<div class="flex flex-col gap-1">
											<p class="font-bold text-base leading-tight line-clamp-2">
												{book.title}
											</p>
											<p
												class="-mt-0.5 text-sm font-medium text-base-content/50 leading-tight line-clamp-1"
											>
												{book.author}
											</p>
										</div>
									</div>
								</div>
							</button>
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
					<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
						{#each library as book}
							<button
								onclick={() => openBook(book.id)}
								class="card w-full bg-base-200 border border-base-300 hover:border-secondary hover:shadow-lg transition-all duration-200 cursor-pointer text-left p-4"
							>
								<div class="flex flex-col gap-4">
									<div
										class="aspect-[3/4] w-full bg-base-300 rounded-lg flex items-center justify-center"
									>
										<Book class="h-12 w-12 text-secondary" />
									</div>
									<div class="flex flex-col gap-1">
										<p class="font-bold text-base leading-tight line-clamp-2">{book.title}</p>
										<p class="text-sm font-medium text-base-content/50 leading-tight line-clamp-1">
											{book.author}
										</p>
									</div>
								</div>
							</button>
						{/each}
					</div>
				</section>
			{/if}
		{/if}
	</div>
</div>

<LanguageSelector bind:open={showLanguageModal} />
