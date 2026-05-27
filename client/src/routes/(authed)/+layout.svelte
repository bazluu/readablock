<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { baseURL } from '$lib/state.svelte.js';
	import Navbar from '$lib/components/Navbar.svelte';

	onMount(async () => {
		const response = await fetch(`${baseURL}/app/dashboard/books`, {
			credentials: 'include'
		});
		if (response.status === 401 || response.status === 403) {
			goto('/login');
		}
	});
</script>

{#if !$page.url.pathname.startsWith('/read')}
	<Navbar />
{/if}

<slot />
