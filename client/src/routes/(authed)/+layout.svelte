<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { baseURL } from '$lib/state.svelte.js';
	import Navbar from '$lib/components/Navbar.svelte';

	let authed = $state(null);

	onMount(async () => {
		try {
			const response = await fetch(`${baseURL}/app/user`, {
				credentials: 'include'
			});
			if (response.ok) {
				authed = true;
			} else {
				authed = false;
				goto('/login');
			}
		} catch {
			authed = false;
			goto('/login');
		}
	});
</script>

{#if authed === null}
	<div class="min-h-screen bg-base-100 flex items-center justify-center">
		<span class="loading loading-spinner loading-lg"></span>
	</div>
{:else if authed}
	{#if !$page.url.pathname.startsWith('/read')}
		<Navbar />
	{/if}

	<slot />
{/if}