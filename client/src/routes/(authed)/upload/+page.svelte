<script>
	import { onMount } from 'svelte';
	import { baseURL } from '$lib/state.svelte.js';

	const ALLOWED_EXTENSIONS = '.epub,.pdf,.txt,.kepub';
	const MAX_FILE_SIZE_MB = 50;
	const MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024;

	const FLAG_EMOJI = {
		it: '🇮🇹',
		de: '🇩🇪',
		en: '🇬🇧',
		fr: '🇫🇷',
		es: '🇪🇸',
		pt: '🇵🇹',
		ru: '🇷🇺',
		zh: '🇨🇳',
		ja: '🇯🇵',
		ko: '🇰🇷',
		ar: '🇸🇦',
		hi: '🇮🇳',
		nl: '🇳🇱',
		pl: '🇵🇱',
		tr: '🇹🇷',
		sv: '🇸🇪',
		da: '🇩🇰',
		fi: '🇫🇮',
		no: '🇳🇴',
		cs: '🇨🇿',
		el: '🇬🇷',
		th: '🇹🇭',
		uk: '🇺🇦',
		ro: '🇷🇴',
		hu: '🇭🇺',
		id: '🇮🇩',
		ms: '🇲🇾',
		vi: '🇻🇳'
	};

	const LANGUAGE_NAMES = {
		it: 'Italian',
		de: 'German',
		en: 'English',
		fr: 'French',
		es: 'Spanish',
		pt: 'Portuguese',
		ru: 'Russian',
		zh: 'Chinese',
		ja: 'Japanese',
		ko: 'Korean',
		ar: 'Arabic',
		hi: 'Hindi',
		nl: 'Dutch',
		pl: 'Polish',
		tr: 'Turkish',
		sv: 'Swedish',
		da: 'Danish',
		fi: 'Finnish',
		no: 'Norwegian',
		cs: 'Czech',
		el: 'Greek',
		th: 'Thai',
		uk: 'Ukrainian',
		ro: 'Romanian',
		hu: 'Hungarian',
		id: 'Indonesian',
		ms: 'Malay',
		vi: 'Vietnamese'
	};

	let title = '';
	let author = '';
	let file = null;
	let fileName = '';
	let language = '';

	let languages = [];

	let errorMessage = '';
	let successMessage = '';
	let isLoading = false;

	onMount(async () => {
		try {
			const response = await fetch(`${baseURL}/app/supported-languages/`, {
				credentials: 'include'
			});
			const data = await response.json();
			languages = data.languages;
		} catch (error) {
			console.error('Failed to load languages:', error);
		}
	});

	function handleFileChange(e) {
		const selected = e.target.files[0];
		if (!selected) {
			file = null;
			fileName = '';
			return;
		}

		if (selected.size > MAX_FILE_SIZE) {
			errorMessage = `File exceeds the ${MAX_FILE_SIZE_MB} MB size limit`;
			file = null;
			fileName = '';
			e.target.value = '';
			return;
		}

		file = selected;
		fileName = selected.name;
		errorMessage = '';
	}

	function handleDrop(e) {
		e.preventDefault();
		const dropped = e.dataTransfer.files[0];
		if (!dropped) return;

		const ext = '.' + dropped.name.split('.').pop().toLowerCase();
		if (!ALLOWED_EXTENSIONS.split(',').includes(ext)) {
			errorMessage = `Invalid file type. Allowed types: ${ALLOWED_EXTENSIONS}`;
			return;
		}

		if (dropped.size > MAX_FILE_SIZE) {
			errorMessage = `File exceeds the ${MAX_FILE_SIZE_MB} MB size limit`;
			return;
		}

		file = dropped;
		fileName = dropped.name;
		errorMessage = '';
	}

	function handleDragOver(e) {
		e.preventDefault();
	}

	function removeFile() {
		file = null;
		fileName = '';
	}

	async function handleSubmit(e) {
		e.preventDefault();
		errorMessage = '';
		successMessage = '';

		if (!file) {
			errorMessage = 'Please select a file to upload';
			return;
		}

		isLoading = true;

		try {
			const formData = new FormData();
			formData.append('title', title);
			formData.append('author', author);
			formData.append('file', file);
			formData.append('language', language);

			const response = await fetch(`${baseURL}/app/books/upload`, {
				method: 'POST',
				credentials: 'include',
				body: formData
			});

			const data = await response.json();

			if (response.ok) {
				successMessage = data.message;
				title = '';
				author = '';
				language = 'it';
				file = null;
				fileName = '';
			} else {
				errorMessage = data.error || 'Upload failed. Please try again.';
			}
		} catch (error) {
			console.error('Upload error:', error);
			errorMessage = 'An error occurred during upload. Please try again.';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Upload Book — readablock</title>
</svelte:head>

<div
	class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/20 via-base-100 to-secondary/20 p-4 overflow-x-hidden"
>
	<div class="card w-full max-w-lg bg-base-100 shadow-2xl">
		<div class="card-body p-6 sm:p-8">
			<!-- Header -->
			<div class="text-center mb-6">
				<h2 class="text-3xl font-bold text-primary mb-2">Upload a Book</h2>
				<p class="text-base-content/60">Add a book to your library (.epub, .pdf, .txt, .kepub)</p>
			</div>

			<!-- Error Message -->
			{#if errorMessage}
				<div class="alert alert-error mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="stroke-current shrink-0 h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<span>{errorMessage}</span>
				</div>
			{/if}

			<!-- Success Message -->
			{#if successMessage}
				<div class="alert alert-success mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="stroke-current shrink-0 h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<span>{successMessage}</span>
					<a href="/dashboard" class="btn btn-sm btn-ghost">Go to Dashboard</a>
				</div>
			{/if}

			<form on:submit={handleSubmit} class="space-y-4">
				<!-- Title -->
				<div class="form-control">
					<label class="label" for="book-title">
						<span class="label-text">Title</span>
					</label>
					<input
						id="book-title"
						type="text"
						placeholder="Book title"
						class="input input-bordered w-full"
						bind:value={title}
						disabled={isLoading}
						required
					/>
				</div>

				<!-- Author -->
				<div class="form-control">
					<label class="label" for="book-author">
						<span class="label-text">Author</span>
					</label>
					<input
						id="book-author"
						type="text"
						placeholder="Author name"
						class="input input-bordered w-full"
						bind:value={author}
						disabled={isLoading}
						required
					/>
				</div>

				<!-- Language -->
				<div class="form-control">
					<label class="label" for="book-language">
						<span class="label-text">Language</span>
					</label>
					<select
						id="book-language"
						class="select select-bordered w-full"
						bind:value={language}
						disabled={isLoading}
					>
				{#each languages as lang}
					<option value={lang.deepl}>
						{lang.name} ({lang.deepl})
					</option>
				{/each}
					</select>
				</div>

				<!-- File Upload -->
				<div class="form-control">
					<label class="label">
						<span class="label-text">Book File</span>
						<span class="label-text-alt text-base-content/50">Max {MAX_FILE_SIZE_MB} MB</span>
					</label>

					{#if fileName}
						<div class="flex items-center gap-3 p-4 bg-base-200 rounded-lg">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-8 w-8 text-primary shrink-0"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
								/>
							</svg>
							<span class="text-sm truncate flex-1">{fileName}</span>
							<button
								type="button"
								class="btn btn-ghost btn-sm btn-circle"
								on:click={removeFile}
								disabled={isLoading}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-4 w-4"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M6 18L18 6M6 6l12 12"
									/>
								</svg>
							</button>
						</div>
					{:else}
						<!-- svelte-ignore a11y-no-static-element-interactions -->
						<div
							class="border-2 border-dashed border-base-content/20 rounded-lg p-8 text-center cursor-pointer hover:border-primary hover:bg-base-200 transition-colors"
							on:drop={handleDrop}
							on:dragover={handleDragOver}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-10 w-10 mx-auto mb-3 text-base-content/40"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
								/>
							</svg>
							<p class="text-base-content/60 mb-2">Drag and drop your file here, or</p>
							<label class="btn btn-outline btn-sm btn-primary" for="file-input">
								Browse Files
							</label>
							<input
								id="file-input"
								type="file"
								accept={ALLOWED_EXTENSIONS}
								class="hidden"
								on:change={handleFileChange}
								disabled={isLoading}
							/>
						</div>
					{/if}
				</div>

				<!-- Submit -->
				<div class="form-control mt-6">
					<button type="submit" class="btn btn-primary w-full" disabled={isLoading || !file}>
						{#if isLoading}
							<span class="loading loading-spinner"></span>
							Uploading...
						{:else}
							Upload Book
						{/if}
					</button>
				</div>
			</form>

			<!-- Back Link -->
			<div class="text-center mt-6">
				<a href="/dashboard" class="btn btn-sm btn-outline text-base-content/60">
					Back to Dashboard
				</a>
			</div>
		</div>
	</div>
</div>
