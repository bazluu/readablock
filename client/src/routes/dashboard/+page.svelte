<script>
	import { onMount } from 'svelte';
	const baseURL = 'http://127.0.0.1:8000';

	let continueReading = [];
	let library = [];
	let isLoading = true;
	let error = null;

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

<div class="min-h-screen bg-base-100 text-base-content p-8">
	<div class="max-w-6xl mx-auto">
		<h1 class="font-display text-4xl font-bold mb-8">Your Dashboard</h1>

		{#if isLoading}
			<div class="flex justify-center items-center h-64">
				<span class="loading loading-spinner loading-lg"></span>
			</div>
		{:else if error}
			<div class="alert alert-error">
				<span>Error: {error}</span>
			</div>
		{:else}
			{#if continueReading.length > 0}
				<section class="mb-12">
					<h2 class="font-display text-2xl font-bold mb-6 flex items-center gap-2">
						<span>📖</span> Continue Reading
					</h2>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
						{#each continueReading as book}
							<a
								href="/read?id={book.id}"
								class="card bg-base-200 hover:bg-base-300 transition-colors cursor-pointer border-2 border-amber-600"
							>
								<div class="card-body">
									<h3 class="card-title text-lg">{book.title}</h3>
									<p class="text-base-content/70">{book.author}</p>
									<div class="mt-2">
										<progress
											class="progress progress-primary w-full"
											value={book.sentence_last_read}
											max="100"
										></progress>
										<p class="text-xs text-base-content/50 mt-1">
											Sentence {book.sentence_last_read}
										</p>
									</div>
								</div>
							</a>
						{/each}
					</div>
				</section>
			{/if}

			{#if library.length > 0}
				<section>
					<h2 class="font-display text-2xl font-bold mb-6 flex items-center gap-2">
						<span>📚</span> Your Library
					</h2>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
						{#each library as book}
							<a
								href="/read?id={book.id}"
								class="card bg-base-200 hover:bg-base-300 transition-colors cursor-pointer border-2 border-base-300 hover:border-amber-600"
							>
								<div class="card-body">
									<h3 class="card-title text-lg">{book.title}</h3>
									<p class="text-base-content/70">{book.author}</p>
								</div>
							</a>
						{/each}
					</div>
				</section>
			{/if}

			{#if continueReading.length === 0 && library.length === 0}
				<div class="text-center py-16">
					<p class="text-xl text-base-content/60 mb-4">No books yet</p>
					<a href="/read" class="btn btn-primary">Start Reading</a>
				</div>
			{/if}
		{/if}
	</div>
</div>
