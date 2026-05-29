<script>
	import { onMount } from 'svelte';
	import { baseURL, selectedLanguage } from '$lib/state.svelte.js';
	import Modal from './Modal.svelte';

	let { open = $bindable(false) } = $props();
	let languages = $state([]);

	onMount(async () => {
		const response = await fetch(`${baseURL}/app/supported-languages`, {
			credentials: 'include'
		});
		if (response.ok) {
			const data = await response.json();
			languages = data.languages;
		}
	});

	function selectLanguage(deepl) {
		selectedLanguage.value = deepl;
		open = false;
	}
</script>

<Modal bind:open title="Select Language" closable={false}>
	<div class="list bg-base-200 rounded-box text-left items-left overflow-y-auto max-h-[60vh]">
		{#each languages as lang}
			<div
				class="list-row cursor-pointer hover:bg-base-300"
				onclick={() => selectLanguage(lang.deepl)}
			>
				<span class="">{lang.name}</span>
			</div>
		{/each}
	</div>
</Modal>
