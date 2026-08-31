<script>
	import { onMount } from 'svelte';
	import { baseURL, selectedLanguage } from '$lib/state.svelte.js';
	import PageHeader from '$lib/components/PageHeader.svelte';

	const ALLOWED_EXTENSIONS = '.epub';
	const MAX_FILE_SIZE_MB = 50;
	const MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024;

	let title = '';
	let author = '';
	let file = null;
	let fileName = '';
	let language = '';
	let isPublic = false;
	let description = '';
	let readingEaseScore = '';
	let isSuperuser = false;
	let content = '';

	let languages = [];

	let errorMessage = '';
	let successMessage = '';
	let isLoading = false;

	onMount(async () => {
		if (!language && selectedLanguage.value) {
			language = selectedLanguage.value;
		}

		try {
			const response = await fetch(`${baseURL}/app/supported-languages`, {
				credentials: 'include'
			});
			const data = await response.json();
			languages = data.languages;
		} catch (error) {
			console.error('Failed to load languages:', error);
		}

		try {
			const userResponse = await fetch(`${baseURL}/app/user`, {
				credentials: 'include'
			});
			if (userResponse.ok) {
				const userData = await userResponse.json();
				isSuperuser = userData.is_superuser || false;
			}
		} catch (error) {
			console.error('Failed to load user data:', error);
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

	async function handlePasteFromClipboard() {
		try {
			const text = await navigator.clipboard.readText();
			content = text;
			errorMessage = '';
		} catch {
			errorMessage = 'Unable to access clipboard. Please paste manually (Ctrl+V).';
		}
	}

	function clearContent() {
		content = '';
	}

	async function handleSubmit(e) {
		e.preventDefault();
		errorMessage = '';
		successMessage = '';

		if (!file && !content.trim()) {
			errorMessage = 'Please select a file or paste text content';
			return;
		}

		isLoading = true;

		try {
			let response;

			if (content.trim()) {
				const body = {
					title,
					author,
					language,
					content,
					is_public: isPublic,
					description
				};
				if (readingEaseScore !== '') {
					body.reading_ease_score = readingEaseScore;
				}

				response = await fetch(`${baseURL}/app/books/upload-content`, {
					method: 'POST',
					credentials: 'include',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify(body)
				});
			} else {
				const formData = new FormData();
				formData.append('title', title);
				formData.append('author', author);
				formData.append('file', file);
				formData.append('language', language);
				formData.append('is_public', isPublic);
				formData.append('description', description);
				if (readingEaseScore !== '') {
					formData.append('reading_ease_score', readingEaseScore);
				}

				response = await fetch(`${baseURL}/app/books/upload-file`, {
					method: 'POST',
					credentials: 'include',
					body: formData
				});
			}

			const data = await response.json();

			if (response.ok) {
				successMessage = data.message;
				title = '';
				author = '';
				language = selectedLanguage.value || '';
				isPublic = false;
				description = '';
				readingEaseScore = '';
				file = null;
				fileName = '';
				content = '';
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

<div class="min-h-screen bg-base-100">
	<PageHeader title="Upload a Book" subtitle="Add a book to your library (.epub or paste text)" />

	<div class="flex items-center justify-center p-4">
		<div class="card w-full max-w-lg bg-base-200 border border-base-300">
			<div class="card-body p-6 sm:p-8">
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
							class="input input-bordered w-full box-border"
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
							class="input input-bordered w-full box-border"
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

					<!-- Description -->
					<div class="form-control">
						<label class="label" for="book-description">
							<span class="label-text">Description</span>
						</label>
						<textarea
							id="book-description"
							placeholder="Book description"
							class="textarea textarea-bordered w-full box-border"
							bind:value={description}
							disabled={isLoading}
						></textarea>
					</div>

					{#if isSuperuser}
						<!-- Reading Ease Score (Superuser Only) -->
						<div class="form-control">
							<label class="label" for="reading-ease-score">
								<span class="label-text">Reading Ease Score</span>
							</label>
							<input
								id="reading-ease-score"
								type="number"
								step="0.1"
								placeholder="e.g. 75.5"
								class="input input-bordered w-full box-border"
								bind:value={readingEaseScore}
								disabled={isLoading}
							/>
						</div>

						<!-- Public Book (Superuser Only) -->
						<div class="form-control">
							<label class="label cursor-pointer justify-start gap-3">
								<input
									type="checkbox"
									class="checkbox checkbox-primary"
									bind:checked={isPublic}
									disabled={isLoading}
								/>
								<span class="label-text">Make this book public</span>
							</label>
						</div>
					{/if}

					<!-- Text Content -->
					{#if !fileName}
						<div class="form-control">
							<label class="label" for="book-content">
								<span class="label-text">Book Text</span>
								<span class="label-text-alt text-base-content/50">Paste or type content</span>
							</label>
							<textarea
								id="book-content"
								placeholder="Paste or type your book content here..."
								class="textarea textarea-bordered w-full box-border min-h-[150px]"
								bind:value={content}
								disabled={isLoading}
							></textarea>
							<div class="flex gap-2 mt-2">
								<button
									type="button"
									class="btn btn-outline btn-sm btn-primary"
									on:click={handlePasteFromClipboard}
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
											d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
										/>
									</svg>
									Paste from Clipboard
								</button>
								<button
									type="button"
									class="btn btn-ghost btn-sm"
									on:click={clearContent}
									disabled={isLoading || !content}
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
									Clear
								</button>
							</div>
						</div>
					{/if}

					{#if !content && !fileName}
						<div class="divider">or</div>
					{/if}

					<!-- File Upload -->
					{#if !content}
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
					{/if}

					<!-- Submit -->
					<div class="form-control mt-6">
						<button
							type="submit"
							class="btn btn-primary w-full"
							disabled={isLoading || (!file && !content.trim())}
						>
							{#if isLoading}
								<span class="loading loading-spinner"></span>
								Uploading...
							{:else}
								Upload Book
							{/if}
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</div>
