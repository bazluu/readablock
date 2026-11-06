<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { baseURL, selectedBookId, selectedLanguage } from '$lib/state.svelte.js';
	import { AlertCircle, ChevronDown, Languages, Library, RotateCcw, Upload } from 'lucide-svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import BookCard from '$lib/components/BookCard.svelte';
	import DeleteBookModal from '$lib/components/DeleteBookModal.svelte';

	const SORT_FIELDS = [
		{ field: 'alphabetical', label: 'Title', asc: 'alphabetical_asc', desc: 'alphabetical_desc' },
		{ field: 'author', label: 'Author', asc: 'author_asc', desc: 'author_desc' },
		{ field: 'date_added', label: 'Date added', asc: 'date_added_asc', desc: 'date_added_desc' }
	];

	let library = $state([]);
	let isLoading = $state(true);
	let error = $state(null);
	let sortBy = $state('alphabetical');
	let sortDescending = $state(false);
	let showDeleteModal = $state(false);
	let bookToDelete = $state(null);

	// Language dropdown, mirroring the navbar's picker. It shows "All" when no
	// language is selected; picking a language (or "All") writes the navbar's
	// selectedLanguage state, which drives the refetch.
	let languages = $state([]);
	let langDropdownOpen = $state(false);

	onMount(async () => {
		const response = await fetch(`${baseURL}/app/supported-languages`, {
			credentials: 'include'
		});
		if (response.ok) {
			const data = await response.json();
			languages = data.languages;
		}
	});

	function clickOutside(node, callback) {
		const handleClick = (event) => {
			if (!node.contains(event.target)) {
				callback();
			}
		};
		document.addEventListener('click', handleClick, true);
		return {
			destroy() {
				document.removeEventListener('click', handleClick, true);
			}
		};
	}

	function selectLanguage(code) {
		selectedLanguage.value = code;
		langDropdownOpen = false;
	}

	function currentLanguageName() {
		if (!selectedLanguage.value) return 'All';
		const lang = languages.find((l) => l.code === selectedLanguage.value);
		return lang ? lang.name : 'All';
	}

	// Maps the field + direction picks onto the endpoint's sort values
	// (alphabetical_asc, author_desc, date_added_asc, ...).
	let sortValue = $derived(
		SORT_FIELDS.find((option) => option.field === sortBy)[sortDescending ? 'desc' : 'asc']
	);

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

	async function addToCollection(bookId) {
		try {
			const response = await fetch(`${baseURL}/app/books/collection`, {
				method: 'POST',
				credentials: 'include',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ book_id: bookId })
			});
			if (!response.ok) {
				throw new Error('Failed to add book to dashboard');
			}
			await fetchBooks();
		} catch (err) {
			console.error('Error adding book to dashboard:', err);
		}
	}

	async function removeFromCollection(bookId) {
		try {
			const response = await fetch(`${baseURL}/app/books/collection/${bookId}`, {
				method: 'DELETE',
				credentials: 'include'
			});
			if (!response.ok) {
				throw new Error('Failed to remove book from dashboard');
			}
			await fetchBooks();
		} catch (err) {
			console.error('Error removing book from dashboard:', err);
		}
	}

	function toggleCollection(book) {
		if (book.in_collection) {
			return removeFromCollection(book.id);
		}
		return addToCollection(book.id);
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

	// Monotonic id per fetchBooks call; responses from superseded requests are
	// discarded so a slow earlier fetch can't overwrite the current filter's
	// results.
	let fetchSequence = 0;

	async function fetchBooks() {
		const requestId = ++fetchSequence;
		isLoading = true;
		error = null;
		try {
			// Follow the language picked in the navbar. Before a language is
			// selected, the endpoint is called without one and lists books in
			// every language.
			const language = selectedLanguage.value ? `&language=${selectedLanguage.value}` : '';
			const response = await fetch(`${baseURL}/app/library?sort=${sortValue}${language}`, {
				credentials: 'include'
			});
			if (!response.ok) {
				throw new Error('Failed to fetch books');
			}
			const data = await response.json();

			if (requestId !== fetchSequence) return;
			library = data.library || [];
		} catch (err) {
			if (requestId !== fetchSequence) return;
			error = err.message;
			console.error('Error fetching books:', err);
		} finally {
			if (requestId === fetchSequence) {
				isLoading = false;
			}
		}
	}

	$effect(() => {
		fetchBooks();
	});

	function openBook(id) {
		selectedBookId.value = id;
		goto('/read');
	}
</script>

<svelte:head>
	<title>Library — readablock</title>
</svelte:head>

<div class="min-h-screen bg-base-100">
	<PageHeader title="Library" subtitle="Every book you can read, in the language of your choice." />

	<div class="max-w-6xl mx-auto px-8 py-10">
		<!-- Filter controls -->
		<div class="flex flex-wrap items-center gap-3 mb-8">
			<div class="relative" use:clickOutside={() => (langDropdownOpen = false)}>
				<button
					onclick={() => (langDropdownOpen = !langDropdownOpen)}
					class="btn inline-flex items-center gap-1.5 px-2.5 py-2 rounded-lg"
				>
					<Languages class="h-4 w-4 sm:h-5 sm:w-5" />
					{currentLanguageName()}
					<ChevronDown class="h-4 w-4 opacity-60" />
				</button>
				{#if langDropdownOpen}
					<div
						class="absolute top-full left-0 mt-1 bg-base-200 border border-base-300 rounded-lg shadow-lg z-50 w-52 overflow-y-auto max-h-64"
					>
						<button
							class="w-full text-left px-4 py-2 btn {!selectedLanguage.value ? 'btn-neutral' : ''}"
							onclick={() => selectLanguage(null)}
						>
							All languages
						</button>
						{#each languages as lang}
							<button
								class="w-full text-left px-4 py-2 btn {selectedLanguage.value === lang.code
									? 'btn-neutral'
									: ''}"
								onclick={() => selectLanguage(lang.code)}
							>
								{lang.name}
							</button>
						{/each}
					</div>
				{/if}
			</div>
			<div class="flex items-center gap-2">
				<span class="text-sm text-base-content/60">Sort</span>
				<select class="select select-sm bg-base-200 border-base-300" bind:value={sortBy}>
					{#each SORT_FIELDS as option (option.field)}
						<option value={option.field}>{option.label}</option>
					{/each}
				</select>
			</div>
			<div class="flex items-center gap-2">
				<span class="text-sm text-base-content/60">Order</span>
				<select class="select select-sm bg-base-200 border-base-300" bind:value={sortDescending}>
					<option value={false}>Ascending</option>
					<option value={true}>Descending</option>
				</select>
			</div>
			<div class="badge badge-secondary badge-soft">{library.length}</div>
		</div>

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
		{:else if library.length === 0}
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
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
				{#each library as book (book.id)}
					<div class="relative">
						<BookCard
							{book}
							onopen={openBook}
							onunread={markUnread}
							ondownload={downloadBook}
							ondelete={requestDelete}
							ontogglecollection={toggleCollection}
						/>
						<div class="badge badge-sm badge-neutral absolute top-2 right-2 pointer-events-none">
							{book.language}
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>

<DeleteBookModal bind:open={showDeleteModal} book={bookToDelete} onDeleted={fetchBooks} />
