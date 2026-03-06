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

<div class="min-h-screen bg-base-100 text-base-content">
	<div class="hero bg-base-200 py-12">
		<div class="hero-content text-center">
			<div class="max-w-2xl">
				<h1 class="font-display text-5xl font-bold text-primary">Your Dashboard</h1>
				<p class="py-6 text-lg text-base-content/70">
					Continue your reading journey or explore your library
				</p>
				<div class="stats stats-vertical sm:stats-horizontal shadow-lg bg-base-100">
					{#if continueReading.length > 0}
						<div class="stat">
							<div class="stat-title">Continue Reading</div>
							<div class="stat-value text-primary">{continueReading.length}</div>
						</div>
					{/if}
					<div class="stat">
						<div class="stat-title">Library</div>
						<div class="stat-value text-secondary">{library.length}</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="max-w-6xl mx-auto p-8">
		{#if isLoading}
			<div class="flex justify-center items-center h-64">
				<span class="loading loading-spinner loading-lg text-primary"></span>
			</div>
		{:else if error}
			<div class="alert alert-error shadow-lg">
				<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
				<span>Error: {error}</span>
			</div>
		{:else}
			{#if continueReading.length > 0}
				<section class="mb-12">
					<div class="flex items-center gap-2 mb-6">
						<span class="badge badge-lg badge-primary">📖</span>
						<h2 class="font-display text-2xl font-bold">Continue Reading</h2>
					</div>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
						{#each continueReading as book}
							<a
								href="/read?id={book.id}"
								class="card bg-base-200 hover:bg-base-300 transition-all duration-300 cursor-pointer hover:scale-[1.02] hover:shadow-xl border-2 border-transparent hover:border-primary"
							>
								<div class="card-body">
									<h3 class="card-title text-lg line-clamp-2">{book.title}</h3>
									<p class="text-base-content/60 text-sm">{book.author}</p>
									<div class="mt-3">
										<div class="flex justify-between text-xs mb-1">
											<span class="text-base-content/50">Progress</span>
											<span class="text-primary font-semibold">{book.sentence_last_read}%</span>
										</div>
										<progress
											class="progress progress-primary w-full"
											value={book.sentence_last_read}
											max="100"
										></progress>
									</div>
									<div class="card-actions justify-end mt-2">
										<button class="btn btn-primary btn-sm">Continue</button>
									</div>
								</div>
							</a>
						{/each}
					</div>
				</section>
			{/if}

			{#if library.length > 0}
				<section>
					<div class="flex items-center gap-2 mb-6">
						<span class="badge badge-lg badge-secondary">📚</span>
						<h2 class="font-display text-2xl font-bold">Your Library</h2>
					</div>
					<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
						{#each library as book}
							<a
								href="/read?id={book.id}"
								class="card bg-base-200 hover:bg-base-300 transition-all duration-300 cursor-pointer hover:scale-[1.02] hover:shadow-md border-2 border-transparent hover:border-secondary"
							>
								<figure class="px-4 pt-4">
									<div class="aspect-[2/3] bg-base-300 rounded-lg flex items-center justify-center">
										<span class="text-4xl">📖</span>
									</div>
								</figure>
								<div class="card-body p-4">
									<h3 class="card-title text-sm line-clamp-2">{book.title}</h3>
									<p class="text-xs text-base-content/60 line-clamp-1">{book.author}</p>
								</div>
							</a>
						{/each}
					</div>
				</section>
			{/if}

			{#if continueReading.length === 0 && library.length === 0}
				<div class="card bg-base-200 max-w-md mx-auto shadow-xl">
					<div class="card-body text-center">
						<figure class="px-10 pt-10">
							<div class="text-6xl">📚</div>
						</figure>
						<h2 class="font-display text-2xl font-bold mt-4">No books yet</h2>
						<p class="text-base-content/60 mb-4">Start your reading journey by adding your first book</p>
						<div class="card-actions justify-center pb-8">
							<a href="/read" class="btn btn-primary btn-lg">Start Reading</a>
						</div>
					</div>
				</div>
			{/if}
		{/if}
	</div>
</div>
