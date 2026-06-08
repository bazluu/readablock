<script>
	import PageHeader from '$lib/components/PageHeader.svelte';
	import { baseURL } from '$lib/state.svelte.js';

	const feedbackTypes = [
		{ value: 'general', label: 'General feedback' },
		{ value: 'bug', label: 'Bug report' },
		{ value: 'feature_request', label: 'Feature request' }
	];

	let feedbackType = 'general';
	let body = '';
	let errorMessage = '';
	let successMessage = '';
	let isLoading = false;

	async function handleSubmit(event) {
		event.preventDefault();
		errorMessage = '';
		successMessage = '';

		if (!body.trim()) {
			errorMessage = 'Please enter your feedback before submitting.';
			return;
		}

		isLoading = true;

		try {
			const response = await fetch(`${baseURL}/app/feedback/`, {
				method: 'POST',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					type: feedbackType,
					body
				})
			});

			const data = await response.json();

			if (response.ok) {
				successMessage = data.message;
				feedbackType = 'general';
				body = '';
			} else {
				errorMessage = data.error || 'Unable to submit feedback. Please try again.';
			}
		} catch (error) {
			console.error('Feedback error:', error);
			errorMessage = 'An error occurred while sending feedback. Please try again.';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Feedback — readablock</title>
</svelte:head>

<div class="min-h-screen bg-base-100">
	<PageHeader
		title="Share Feedback"
		subtitle="Report a bug, suggest a feature, or tell us what would improve your experience"
	/>

	<div class="flex items-center justify-center p-4">
		<div class="card w-full max-w-2xl bg-base-200 border border-base-300">
			<div class="card-body p-6 sm:p-8">
				{#if errorMessage}
					<div class="alert alert-error mb-4">
						<span>{errorMessage}</span>
					</div>
				{/if}

				{#if successMessage}
					<div class="alert alert-success mb-4">
						<span>{successMessage}</span>
					</div>
				{/if}

				<form on:submit={handleSubmit} class="space-y-5">
					<div class="tabs tabs-box box-border w-full bg-base-300 p-1">
						{#each feedbackTypes as type}
							<input
								type="radio"
								name="feedback-type"
								class="tab flex-1 m-0"
								aria-label={type.label}
								value={type.value}
								bind:group={feedbackType}
								disabled={isLoading}
							/>
						{/each}
					</div>

					<div class="form-control">
						<div class="relative w-full min-h-60 overflow-hidden">
							<textarea
								id="feedback-body"
								class="textarea box-border w-full min-h-60 overflow-auto p-2 resize-none"
								placeholder="Message (please be as specific as you can)"
								bind:value={body}
								disabled={isLoading}
								required
							></textarea>
						</div>
					</div>

					<div class="form-control mt-6">
						<button type="submit" class="btn btn-primary w-full" disabled={isLoading}>
							{#if isLoading}
								<span class="loading loading-spinner"></span>
								Sending...
							{:else}
								Submit Feedback
							{/if}
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</div>
