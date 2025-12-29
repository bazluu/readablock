<script>
	import { onMount } from 'svelte';
	const baseURL = 'http://127.0.0.1:8000';
	let sentences = [];
	let sentenceLastRead = 0;
	let sentenceCount = 0;
	let sentenceFirst = 0;
	let hasPrevious = false;
	let isLoading = true;
	let error = null;

	async function getSentences(pageTurn = null) {
		isLoading = true;
		error = null;
		try {
			const response = await fetch(`${baseURL}/app/read/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					sentence_last_read: sentenceLastRead,
					page_turn: pageTurn
				})
			});
			if (!response.ok) {
				throw new Error('Failed to fetch sentences');
			}
			const data = await response.json();
			sentences = data.sentences;
			sentenceLastRead = data.sentence_last_read;
			sentenceCount = data.sentence_count;
			sentenceFirst = data.sentence_first;
			hasPrevious = data.has_previous;
		} catch (err) {
			error = err.message;
			console.error('Error fetching sentences:', err);
		} finally {
			isLoading = false;
		}
	}

	onMount(async () => {
		await getSentences();
	});

	const handleNextPage = async () => {
		await getSentences('next');
	};

	const handlePreviousPage = async () => {
		await getSentences('previous');
	};

	const splitWords = (sentence) => {
		return sentence.split(/(\s+)/);
	};

	const handleWordClick = (word) => {
		alert(`You clicked: "${word}"`);
	};

	const handleTranslate = (sentence) => {
		alert(`Translate: "${sentence}"`);
	};
</script>

<div class="min-h-screen bg-base-100 text-base-content p-4">
	{#if isLoading}
		<div class="flex justify-center items-center h-64">
			<p class="text-lg">Loading sentences...</p>
		</div>
	{:else if error}
		<p class="text-error text-center">Error: {error}</p>
	{:else if sentences.length === 0}
		<p class="text-center">No sentences found.</p>
	{:else}
		<div class="max-w-4xl mx-auto">
			<progress
				class="progress progress-primary w-full"
				value={sentenceLastRead}
				max={sentenceCount}
			></progress>

			<!-- Sentences Table -->
			<div class="overflow-x-auto">
				<table class="table w-full border-collapse">
					<tbody>
						{#each sentences as sentence, index}
							<tr>
								<td class="border border-base-300 px-2 py-2">
									{#each splitWords(sentence) as part}
										{#if part.trim().length > 0}
											<button
												class="btn btn-ghost btn-xs normal-case p-0 m-0.5 hover:bg-base-300"
												on:click={() => handleWordClick(part)}
											>
												{part}
											</button>
										{:else}
											{part}
										{/if}
									{/each}
								</td>
								<td class="border border-base-300 w-12 text-center">
									<button class="btn btn-ghost btn-xs" on:click={() => handleTranslate(sentence)}>
										⬇️
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<!-- Pagination Controls Bottom -->
			<div class="flex justify-between items-center mt-4">
				<button
					class="btn btn-primary"
					on:click={handlePreviousPage}
					disabled={!hasPrevious || isLoading}
				>
					← Previous
				</button>
				<span class="text-sm">Sentences {sentenceFirst + 1} - {sentenceLastRead + 1}</span>
				<button class="btn btn-primary" on:click={handleNextPage} disabled={isLoading}>
					Next →
				</button>
			</div>
		</div>
	{/if}
</div>
