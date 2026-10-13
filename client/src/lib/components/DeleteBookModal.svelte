<script>
	import { baseURL } from '$lib/state.svelte.js';
	import Modal from './Modal.svelte';

	let { open = $bindable(false), book = null, onDeleted } = $props();

	let deleting = $state(false);
	let error = $state(null);

	$effect(() => {
		if (open) {
			deleting = false;
			error = null;
		}
	});

	async function confirmDelete() {
		deleting = true;
		error = null;
		try {
			const response = await fetch(`${baseURL}/app/books/${book.id}`, {
				method: 'DELETE',
				credentials: 'include'
			});
			const data = await response.json();
			if (!response.ok) {
				throw new Error(data.error || 'Failed to delete book');
			}
			onDeleted?.();
			open = false;
		} catch (err) {
			error = err.message;
			console.error('Error deleting book:', err);
		} finally {
			deleting = false;
		}
	}
</script>

<Modal bind:open title="Delete book" closable={false}>
	<div class="flex flex-col gap-4">
		<div class="flex flex-col text-base">
			<p>
				Are you sure you want to delete
				<span class="font-bold">{book?.title_en || book?.title}</span>?
			</p>
			<p class="text-base-content/60">This action cannot be undone.</p>
		</div>

		{#if error}
			<div role="alert" class="alert alert-error">
				<span>{error}</span>
			</div>
		{/if}

		<div class="flex w-full gap-2">
			<button class="btn flex-1" onclick={() => (open = false)} disabled={deleting}> Cancel </button>
			<button class="btn btn-error flex-1" onclick={confirmDelete} disabled={deleting}>
				{#if deleting}
					<span class="loading loading-spinner loading-sm"></span>
					Deleting...
				{:else}
					Delete
				{/if}
			</button>
		</div>
	</div>
</Modal>