<script>
	let { title, subtitle } = $props();
</script>

<div class="bg-base-200 border-b border-base-300">
	<div class="max-w-6xl mx-auto px-8 py-2">
		<h1 class="font-display text-4xl font-bold text-primary">{title}</h1>
		<p class="mt-2 text-base-content/60">{subtitle}</p>
	</div>
</div>
