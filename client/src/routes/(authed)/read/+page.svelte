<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { baseURL, selectedBookId, lastReadBookId, ttsSpeed } from '$lib/state.svelte.js';
	import {
		Languages,
		ChevronLeft,
		ChevronRight,
		ArrowLeft,
		Volume2,
		Minus,
		Plus,
		X
	} from 'lucide-svelte';

	let sentence = null;
	let translated = null; // Translation of the current sentence
	let sentenceCount = 0;
	let sentenceFirst = 0;
	let hasPrevious = false;
	let bookId = null;
	let isLoading = true;
	let error = null;

	// Translation state
	let translating = false;
	let targetLang = 'EN-GB';
	let sourceLang = 'IT';

	// TTS state
	let speaking = false;
	let currentAudio = null;

	function increaseTtsSpeed() {
		ttsSpeed.value = Math.min(1.5, Math.round((ttsSpeed.value + 0.1) * 10) / 10);
	}

	function decreaseTtsSpeed() {
		ttsSpeed.value = Math.max(0.4, Math.round((ttsSpeed.value - 0.1) * 10) / 10);
	}

	// Word translation dropdown state
	let wordDropdown = {
		visible: false,
		word: '',
		translation: '',
		loading: false,
		x: 0,
		y: 0
	};

	function resolveBookId() {
		const params = new URLSearchParams(window.location.search);
		const queryBookId = Number(params.get('id'));

		if (Number.isInteger(queryBookId) && queryBookId > 0) {
			selectedBookId.value = queryBookId;
			return queryBookId;
		}

		const stateBookId = Number(selectedBookId.value);
		if (Number.isInteger(stateBookId) && stateBookId > 0) {
			return stateBookId;
		}

		const lastBookId = Number(lastReadBookId.value);
		if (Number.isInteger(lastBookId) && lastBookId > 0) {
			return lastBookId;
		}

		return null;
	}

	async function getSentences(pageTurn = null) {
		isLoading = true;
		error = null;

		if (bookId === null) {
			bookId = resolveBookId();
		}

		if (bookId === null) {
			error = 'No book selected';
			isLoading = false;
			return;
		}

		try {
			const response = await fetch(`${baseURL}/app/read/`, {
				method: 'POST',
				credentials: 'include',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					book_id: bookId,
					sentence_last_read: sentenceFirst,
					page_turn: pageTurn
				})
			});
			if (!response.ok) {
				throw new Error('Failed to fetch sentence');
			}
			const data = await response.json();
			sentence = data.sentence;
			sentenceCount = data.sentence_count;
			sentenceFirst = data.sentence_first;
			hasPrevious = data.has_previous;
			translated = null;
			lastReadBookId.value = bookId;
		} catch (err) {
			error = err.message;
			console.error('Error fetching sentences:', err);
		} finally {
			isLoading = false;
		}
	}

	async function translateText(text, context = null) {
		try {
			const requestBody = {
				text: text,
				source: sourceLang,
				target: targetLang
			};

			// Add context if provided
			if (context) {
				requestBody.context = context;
			}

			const response = await fetch(`${baseURL}/app/translate/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(requestBody)
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

	async function translateCurrentSentence() {
		// Close translation if it's already open for this sentence
		if (translated) {
			translated = null;
			return;
		}

		translating = true;

		try {
			const result = await translateText(sentence);
			translated = result;
		} catch (err) {
			console.error('Translation error:', err);
			alert(`Translation error: ${err.message}`);
		} finally {
			translating = false;
		}
	}

	async function handleWordClick(event, word, sentenceContext) {
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
			const translated = await translateText(cleanWord, sentenceContext);
			console.log('Translated word:', translated); // Debug log
			wordDropdown = {
				...wordDropdown,
				translation: translated,
				loading: false
			};
			handleSpeak(cleanWord, 'word');
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
		bookId = resolveBookId();
		if (bookId === null) {
			goto('/dashboard');
			return;
		}
		await getSentences();

		// Add global click listener
		document.addEventListener('click', handleGlobalClick);

		return () => {
			document.removeEventListener('click', handleGlobalClick);
		};
	});

	const handleStopSpeaking = () => {
		if (currentAudio) {
			currentAudio.pause();
			currentAudio = null;
		}
		speaking = false;
	};

	const handleNextPage = async () => {
		handleStopSpeaking();
		translated = null; // Clear translation when changing sentences
		closeWordDropdown();
		await getSentences('next');
	};

	const handlePreviousPage = async () => {
		handleStopSpeaking();
		translated = null; // Clear translation when changing sentences
		closeWordDropdown();
		await getSentences('previous');
	};

	const splitWords = (text) => {
		return text.split(/(\s+)/);
	};

	const handleSpeak = async (text) => {
		if (speaking) return;
		speaking = true;

		try {
			const response = await fetch(`${baseURL}/app/tts/`, {
				method: 'POST',
				credentials: 'include',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ text: text, language: sourceLang })
			});

			if (!response.ok) {
				let message = `TTS request failed (HTTP ${response.status})`;
				try {
					const errData = await response.json();
					if (errData.error) message = errData.error;
				} catch {}
				throw new Error(message);
			}

			const data = await response.json();
			const audio = new Audio(`data:audio/mp3;base64,${data.audio}`);

			currentAudio = audio;
			audio.playbackRate = ttsSpeed.value;
			audio.onended = () => {
				speaking = false;
				currentAudio = null;
			};

			audio.onerror = () => {
				speaking = false;
				currentAudio = null;
			};

			audio.play().catch(() => {});
		} catch (err) {
			console.error('TTS error:', err);
			alert(`Text-to-speech failed: ${err.message}`);
			speaking = false;
			currentAudio = null;
		}
	};
</script>

<svelte:window
	on:keydown={(e) => {
		if (e.key === 'Escape') closeWordDropdown();
		if (e.key === 'ArrowRight' && !isLoading) handleNextPage();
		if (e.key === 'ArrowLeft' && !isLoading && hasPrevious) handlePreviousPage();
	}}
/>

<div class="min-h-screen bg-base-100 text-base-content p-4">
	{#if isLoading}
		<div class="flex justify-center items-center h-64">
			<p class="text-lg">Loading sentences...</p>
		</div>
	{:else if error}
		<p class="text-error text-center">Error: {error}</p>
	{:else if sentence === null}
		<p class="text-center">No sentences found.</p>
	{:else}
		<div class="max-w-4xl mx-auto pb-20">
			<div class="fixed top-0 left-0 right-0 bg-base-100 border-b border-base-300 py-3 px-4 z-40">
				<div class="max-w-4xl mx-auto">
					<div class="flex flex-row w-full justify-between items-end mb-4">
						<button class="btn gap-2" on:click={() => goto('/dashboard')}>
							<ArrowLeft size={20} />
							Books
						</button>
						<div class="flex flex-col items-start">
							<div class="join border border-base-300 rounded-lg overflow-hidden">
								<button
									class="join-item btn border-b-0 border-t-0 border-l-0 border-base-300"
									on:click={decreaseTtsSpeed}
									disabled={ttsSpeed.value <= 0.4}><Minus size={16} /></button
								>
								<button
									class="join-item btn pointer-events-none border-b-0 border-t-0 border-base-300"
									>{ttsSpeed.value.toFixed(1)}x</button
								>
								<button
									class="join-item btn border-b-0 border-t-0 border-r-0 border-base-300"
									on:click={increaseTtsSpeed}
									disabled={ttsSpeed.value >= 1.5}><Plus size={16} /></button
								>
							</div>
						</div>
					</div>
					<progress
						class="progress progress-primary w-full mb-1"
						value={sentenceFirst + 1}
						max={sentenceCount}
					></progress>
				</div>
			</div>
			<div class="pt-28">
				<!-- Sentence -->
				<div class="flex flex-col gap-2">
					<div class="rounded-lg flex gap-2">
						<div class="flex-1 border border-base-300 rounded-lg bg-base-200">
							<div class="px-2 pt-1">
								{#each splitWords(sentence) as part}
									{#if part.trim().length > 0}
										<button
											class="btn btn-ghost btn-xs normal-case p-0 m-0.5 hover:bg-base-300 text-lg text-white font-serif"
											on:click={(e) => handleWordClick(e, part, sentence)}
										>
											{part}
										</button>
									{:else}
										{part}
									{/if}
								{/each}
							</div>

							{#if translated}
								<div class="px-4 border-1 bg-primary rounded-b-lg text-black">
									<div class="flex items-start justify-between">
										<div class="flex-1">
											<p class="text-md">{translated}</p>
										</div>
									</div>
								</div>
							{/if}
						</div>
					</div>
				</div>
			</div>

			<!-- Pagination Controls -->
			<div
				class="fixed bottom-0 left-0 right-0 bg-base-100 border-t border-base-300 pb-8 pt-4 px-4 z-40"
			>
				<div class="max-w-4xl mx-auto flex flex-col gap-4">
					<div class="flex justify-center">
						<div class="join join-horizontal my-auto w-full border border-base-300 rounded-lg">
							<button
								class="join-item btn btn-lg flex-1 {translated ? 'btn-primary' : 'btn-ghost'}"
								on:click={translateCurrentSentence}
								disabled={translating}
							>
								{#if translating}
									<span class="loading loading-spinner loading-md"></span>
								{:else}
									<Languages class="h-6 w-6" />
								{/if}
								<p>Translate</p>
							</button>
							<button
								class="join-item btn btn-lg flex-1"
								on:click={() => (speaking ? handleStopSpeaking() : handleSpeak(sentence))}
							>
								{#if speaking}
									<X class="h-6 w-6" />
								{:else}
									<Volume2 class="h-6 w-6" />
								{/if}
								<p>Speech</p>
							</button>
						</div>
					</div>

					<div class="w-full border border-base-300 rounded-lg join join-horizontal items-stretch">
						<button
							class="join-item btn btn-lg"
							on:click={handlePreviousPage}
							disabled={!hasPrevious || isLoading}
						>
							<ChevronLeft />
							<p class="mr-2">PREV</p>
						</button>
						<span
							class="join-item flex-1 flex items-center justify-center text-sm px-4 whitespace-nowrap"
						>
							Sentence {sentenceFirst + 1}
						</span>
						<button class="join-item btn btn-lg" on:click={handleNextPage} disabled={isLoading}>
							<p class="ml-2">NEXT</p>
							<ChevronRight />
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}

	<!-- Word Translation Dropdown -->
	{#if wordDropdown.visible}
		<div
			class="fixed z-50 bg-primary text-accent-content rounded-lg shadow-xl border-2 border-accent-focus px-3 py-2 min-w-[120px] max-w-[300px]"
			style="left: {wordDropdown.x}px; top: {wordDropdown.y}px;"
			on:click={(e) => e.stopPropagation()}
		>
			{#if wordDropdown.loading}
				<div class="flex items-center gap-2">
					<span class="loading loading-spinner loading-xs"></span>
					<span class="text-xs">Translating...</span>
				</div>
			{:else}
				<div class="flex items-center gap-2">
					<div class="space-y-1 flex-1">
						<div class="text-xs font-semibold opacity-70">{wordDropdown.word}</div>
						<div class="text-sm font-bold">{wordDropdown.translation}</div>
					</div>
					<button
						class="btn btn-ghost btn-xs"
						on:click={(e) => {
							e.stopPropagation();
							handleSpeak(wordDropdown.word, 'word');
						}}
					>
						{#if speaking}
							<X size={14} />
						{:else}
							<Volume2 size={14} />
						{/if}
					</button>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
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
