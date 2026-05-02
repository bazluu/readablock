<script>
	import { onMount } from 'svelte';
	import { baseURL, selectedBookId } from '$lib/state.svelte.js';

	let continueReading = $state([]);
	let library = $state([]);
	let isLoading = $state(true);
	let error = $state(null);

	async function fetchBooks() {
		isLoading = true;
		error = null;
		try {
			const response = await fetch(`${baseURL}/app/dashboard/books`, {
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

	onMount(async () => {
		await fetchBooks();
	});
</script>

<svelte:head>
	<title>Dashboard — readablock</title>
</svelte:head>

<div class="min-h-screen bg-base-100">
	<!-- Hero -->
	<div class="bg-base-200 border-b border-base-300">
		<div class="max-w-6xl mx-auto px-8 py-10">
			<h1 class="font-display text-4xl font-bold text-primary">Dashboard</h1>
			<p class="mt-2 text-base-content/60">Continue your reading journey or explore your library.</p>
		</div>
	</div>

	<div class="max-w-6xl mx-auto px-8 py-10">
		{#if isLoading}
			<div class="flex justify-center items-center h-64">
				<span class="loading loading-spinner loading-lg text-primary"></span>
			</div>
		{:else if error}
			<div role="alert" class="alert alert-error">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				<span>{error}</span>
				<button class="btn btn-sm btn-ghost" onclick={fetchBooks}>Retry</button>
			</div>
		{:else if continueReading.length === 0 && library.length === 0}
			<!-- Empty state -->
			<div class="hero min-h-[60vh]">
				<div class="hero-content text-center flex-col">
					<div class="text-7xl mb-4">📚</div>
					<div>
						<h2 class="text-2xl font-bold">No books yet</h2>
						<p class="py-4 text-base-content/60 max-w-sm">
							Start your reading journey by uploading your first book.
						</p>
						<a href="/upload" class="btn btn-primary btn-lg">Upload a book</a>
					</div>
				</div>
			</div>
		{:else}
			<!-- Continue Reading -->
			{#if continueReading.length > 0}
				<section class="mb-12">
					<div class="flex items-center gap-3 mb-6">
						<h2 class="text-xl font-bold text-base-content">Continue Reading</h2>
						<div class="badge badge-primary badge-outline">{continueReading.length}</div>
					</div>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
						{#each continueReading as book}
							<a
								href="/read?id={book.id}"
								onclick={() => (selectedBookId.value = book.id)}
								class="card bg-base-200 border border-base-300 hover:border-primary hover:shadow-lg transition-all duration-200 cursor-pointer"
							>
								<div class="card-body gap-3">
									<h3 class="card-title text-base line-clamp-2 leading-snug">{book.title}</h3>
									<p class="text-sm text-base-content/50">{book.author}</p>
									<div>
										<div class="flex justify-between text-xs mb-1.5">
											<span class="text-base-content/40">Progress</span>
											<span class="font-semibold text-primary">{book.sentence_last_read}%</span>
										</div>
										<progress
											class="progress progress-primary w-full h-1.5"
											value={book.sentence_last_read}
											max="100"
										></progress>
									</div>
									<div class="card-actions justify-end">
										<span class="btn btn-primary btn-sm">Continue</span>
									</div>
								</div>
							</a>
						{/each}
					</div>
				</section>

				<div class="divider"></div>
			{/if}

			<!-- Library -->
			{#if library.length > 0}
				<section>
					<div class="flex items-center gap-3 mb-6">
						<h2 class="text-xl font-bold text-base-content">Your Library</h2>
						<div class="badge badge-secondary badge-outline">{library.length}</div>
					</div>
					<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
						{#each library as book}
							<a
								href="/read?id={book.id}"
								onclick={() => (selectedBookId.value = book.id)}
								class="card bg-base-200 border border-base-300 hover:border-secondary hover:shadow-md transition-all duration-200 cursor-pointer"
							>
								<figure class="px-4 pt-4">
									<div class="aspect-[2/3] w-full bg-base-300 rounded-lg flex items-center justify-center text-3xl">
										📖
									</div>
								</figure>
								<div class="card-body p-3 gap-1">
									<p class="text-sm font-semibold line-clamp-2 leading-snug">{book.title}</p>
									<p class="text-xs text-base-content/50 line-clamp-1">{book.author}</p>
								</div>
							</a>
						{/each}
					</div>
				</section>
			{/if}
		{/if}
	</div>
</div>
