<script>
	import { baseURL } from '$lib/state.svelte.js';
	import Modal from './Modal.svelte';

	let { open = $bindable(false), onSetGoal, currentGoal = null } = $props();

	const goals = [
		{
			amount: 280,
			title: 'A gentle start',
			subtitle: 'Perfect for easing in — a few minutes a day'
		},
		{
			amount: 550,
			title: 'A steady habit',
			subtitle: 'A comfortable routine that fits around life'
		},
		{
			amount: 1370,
			title: 'A serious reader',
			subtitle: 'Consistent daily practice for fast progress'
		},
		{
			amount: 2740,
			title: 'Total immersion',
			subtitle: 'For those who want to live in the language'
		}
	];

	let selected = $state(550);

	$effect(() => {
		if (open && currentGoal) {
			selected = currentGoal;
		}
	});
	let saving = $state(false);
	let error = $state(null);

	async function save() {
		saving = true;
		error = null;
		try {
			const response = await fetch(`${baseURL}/app/update-word-goal`, {
				method: 'POST',
				credentials: 'include',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ word_goal: selected })
			});
			const data = await response.json();
			if (!response.ok) {
				throw new Error(data.error || 'Failed to set goal');
			}
			onSetGoal?.(selected);
			open = false;
		} catch (err) {
			error = err.message;
			console.error('Error setting word goal:', err);
		} finally {
			saving = false;
		}
	}
</script>

<Modal bind:open title="Set daily reading goal" closable={false}>
	<div class="flex flex-col gap-4">
		<div class="flex flex-col gap-2">
			{#each goals as goal}
				<button
					type="button"
					class="btn w-full h-auto min-h-0 py-2 justify-between {selected === goal.amount
						? 'btn-primary'
						: 'btn-outline border-base-300'}"
					onclick={() => (selected = goal.amount)}
				>
					<div class="flex flex-col items-start gap-0.5 normal-case text-left font-normal">
						<span class="font-medium">{goal.amount.toLocaleString()} words</span>
						<span class="text-xs opacity-70">
							{goal.subtitle} — {(goal.amount * 365).toLocaleString()} words a year
						</span>
					</div>
					{#if selected === goal.amount}
						<span class="badge badge-soft whitespace-nowrap">Selected</span>
					{/if}
				</button>
			{/each}
		</div>

		{#if error}
			<div role="alert" class="alert alert-error">
				<span>{error}</span>
			</div>
		{/if}

		<div class="flex w-full gap-2">
			<button class="btn flex-1" onclick={() => (open = false)} disabled={saving}> Close </button>
			<button class="btn btn-primary flex-1" onclick={save} disabled={saving}>
				{#if saving}
					<span class="loading loading-spinner loading-sm"></span>
					Saving...
				{:else}
					Set goal
				{/if}
			</button>
		</div>
	</div>
</Modal>
