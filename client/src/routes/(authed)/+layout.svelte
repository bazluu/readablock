<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { baseURL } from '$lib/state.svelte.js';

	onMount(async () => {
		const response = await fetch(`${baseURL}/app/dashboard/books`, {
			credentials: 'include'
		});
		if (response.status === 401 || response.status === 403) {
			goto('/login');
		}
	});
</script>

<slot />
