<script>
	let { open = $bindable(false), title = '', closable = true, children } = $props();
</script>

<dialog class="modal" {open}>
	<div class="modal-box my-4 max-h-[calc(100vh-10rem)]">
		{#if title}
			<h3 class="text-lg font-bold mb-4">{title}</h3>
		{/if}
		{@render children?.()}
		{#if closable}
			<div class="modal-action">
				<button class="btn" onclick={() => (open = false)}>Close</button>
			</div>
		{/if}
	</div>
	{#if closable}
		<form method="dialog" class="modal-backdrop">
			<button>close</button>
		</form>
	{/if}
</dialog>
