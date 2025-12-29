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

	// Translation state
	let translations = {}; // Store translations by sentence index
	let translatingIndex = null;
	let targetLang = 'EN-GB';
	let sourceLang = 'IT';

	// Word translation dropdown state
	let wordDropdown = {
		visible: false,
		word: '',
		translation: '',
		loading: false,
		x: 0,
		y: 0
	};

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

	async function translateText(text) {
		try {
			const response = await fetch(`${baseURL}/app/translate/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					text: text,
					source: sourceLang,
					target: targetLang
				})
			});

			if (!response.ok) {
				throw new Error('Translation failed');
			}

			const data = await response.json();
			console.log('API Response:', data); // Debug log

			// The API returns: { "translated": "done" }
			// where "translated" is a string, not an object
			return data.translated;
		} catch (err) {
			console.error('Translation error:', err);
			throw err;
		}
	}

	async function translateSentence(sentence, index) {
		translatingIndex = index;
		try {
			const translated = await translateText(sentence);
			translations[index] = {
				original: sentence,
				translated: translated
			};
			translations = { ...translations }; // Trigger reactivity
		} catch (err) {
			console.error('Translation error:', err);
			alert(`Translation error: ${err.message}`);
		} finally {
			translatingIndex = null;
		}
	}

	async function handleWordClick(event, word) {
		event.stopPropagation();

		const cleanWord = word.trim();
		if (cleanWord.length === 0) return;

		// Get button position for dropdown placement
		const rect = event.target.getBoundingClientRect();

		// Show dropdown immediately with loading state
		wordDropdown = {
			visible: true,
			word: cleanWord,
			translation: '',
			loading: true,
			x: rect.left,
			y: rect.bottom + window.scrollY + 4
		};

		try {
			const translated = await translateText(cleanWord);
			console.log('Translated word:', translated); // Debug log
			wordDropdown = {
				...wordDropdown,
				translation: translated,
				loading: false
			};
		} catch (err) {
			console.error('Word translation error:', err);
			wordDropdown = {
				...wordDropdown,
				translation: 'Translation failed',
				loading: false
			};
		}
	}

	function closeWordDropdown() {
		wordDropdown = {
			visible: false,
			word: '',
			translation: '',
			loading: false,
			x: 0,
			y: 0
		};
	}

	// Close dropdown when clicking anywhere
	function handleGlobalClick(event) {
		if (wordDropdown.visible) {
			closeWordDropdown();
		}
	}

	onMount(async () => {
		await getSentences();

		// Add global click listener
		document.addEventListener('click', handleGlobalClick);

		return () => {
			document.removeEventListener('click', handleGlobalClick);
		};
	});

	const handleNextPage = async () => {
		translations = {}; // Clear translations when changing pages
		closeWordDropdown();
		await getSentences('next');
	};

	const handlePreviousPage = async () => {
		translations = {}; // Clear translations when changing pages
		closeWordDropdown();
		await getSentences('previous');
	};

	const splitWords = (sentence) => {
		return sentence.split(/(\s+)/);
	};

	const handleTranslate = async (sentence, index) => {
		await translateSentence(sentence, index);
	};
</script>

<svelte:window on:keydown={(e) => e.key === 'Escape' && closeWordDropdown()} />

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
			<!-- Language Selector -->
			<div class="mb-4 flex gap-4 items-center">
				<label class="form-control w-full max-w-xs">
					<div class="label">
						<span class="label-text">Target Language</span>
					</div>
					<select class="select select-bordered" bind:value={targetLang}>
						<option value="EN-GB">English (UK)</option>
						<option value="EN-US">English (US)</option>
						<option value="ES">Spanish</option>
						<option value="FR">French</option>
						<option value="DE">German</option>
						<option value="IT">Italian</option>
						<option value="PT-PT">Portuguese</option>
						<option value="RU">Russian</option>
						<option value="JA">Japanese</option>
						<option value="ZH">Chinese</option>
					</select>
				</label>
			</div>

			<progress
				class="progress progress-primary w-full mb-4"
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
									<div class="mb-2">
										{#each splitWords(sentence) as part}
											{#if part.trim().length > 0}
												<button
													class="btn btn-ghost btn-xs normal-case p-0 m-0.5 hover:bg-base-300"
													on:click={(e) => handleWordClick(e, part)}
												>
													{part}
												</button>
											{:else}
												{part}
											{/if}
										{/each}
									</div>

									{#if translations[index]}
										<div class="mt-2 p-2 bg-base-200 rounded-lg">
											<div class="flex items-start justify-between">
												<div class="flex-1">
													<p class="text-sm font-semibold text-primary">Translation:</p>
													<p class="text-sm">{translations[index].translated}</p>
												</div>
												<button
													class="btn btn-ghost btn-xs"
													on:click={() => {
														delete translations[index];
														translations = { ...translations };
													}}
												>
													✕
												</button>
											</div>
										</div>
									{/if}
								</td>
								<td class="border border-base-300 w-12 text-center">
									<button
										class="btn btn-ghost btn-xs"
										on:click={() => handleTranslate(sentence, index)}
										disabled={translatingIndex === index}
									>
										{#if translatingIndex === index}
											<span class="loading loading-spinner loading-xs"></span>
										{:else}
											⬇️
										{/if}
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<!-- Pagination Controls -->
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

	<!-- Word Translation Dropdown -->
	{#if wordDropdown.visible}
		<div
			class="fixed z-50 bg-accent text-accent-content rounded-lg shadow-xl border-2 border-accent-focus px-3 py-2 min-w-[120px] max-w-[300px]"
			style="left: {wordDropdown.x}px; top: {wordDropdown.y}px;"
			on:click={(e) => e.stopPropagation()}
		>
			{#if wordDropdown.loading}
				<div class="flex items-center gap-2">
					<span class="loading loading-spinner loading-xs"></span>
					<span class="text-xs">Translating...</span>
				</div>
			{:else}
				<div class="space-y-1">
					<div class="text-xs font-semibold opacity-70">{wordDropdown.word}</div>
					<div class="text-sm font-bold">{wordDropdown.translation}</div>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	/* Optional: Add smooth transition for dropdown */
	.fixed {
		animation: fadeIn 0.15s ease-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(-4px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
