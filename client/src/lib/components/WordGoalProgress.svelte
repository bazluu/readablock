<script>
	let { wordCount = 0, wordGoal = 0, onSetGoal } = $props();

	let clamped = $derived(Math.min(wordCount, wordGoal));
	let exceeded = $derived(wordGoal > 0 && wordCount > wordGoal);
	let percent = $derived(wordGoal > 0 ? Math.round((clamped / wordGoal) * 100) : 0);
	let overBy = $derived(wordCount - wordGoal);
</script>

<div class="flex items-center gap-3" role="status">
	{#if !wordGoal}
		{#if onSetGoal}
			<button
				class="btn btn-ghost flex-1 h-auto min-h-0 flex-col items-stretch gap-1 justify-start px-0 py-1"
				onclick={onSetGoal}
			>
				<progress class="progress h-1.5 w-full" value="0" max="100"></progress>
				<span class="text-xs font-normal normal-case text-left text-base-content/60">
					Set a daily goal
				</span>
			</button>
		{:else}
			<div class="flex-1 flex flex-col gap-1 opacity-70">
				<progress class="progress h-1.5 w-full" value="0" max="100" disabled></progress>
				<span class="text-xs text-base-content/60">Set a daily goal</span>
			</div>
		{/if}
	{:else}
		<div class="flex-1 flex flex-col gap-1">
			<div class="flex items-center gap-3">
				<progress
					class="progress h-1.5 flex-1 {exceeded ? 'progress-success' : 'progress-primary'}"
					value={clamped}
					max={wordGoal}
				></progress>
				{#if exceeded}
					<span class="badge badge-success badge-soft whitespace-nowrap">
						+{overBy.toLocaleString()} over goal
					</span>
				{/if}
			</div>
			<span class="text-xs {exceeded ? 'text-success' : 'text-base-content/60'}">
				{wordCount.toLocaleString()} / {wordGoal.toLocaleString()} words ({percent}%)
			</span>
		</div>
	{/if}
</div>
