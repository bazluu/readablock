<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { baseURL } from '$lib/state.svelte.js';
	import Navbar from '$lib/components/Navbar.svelte';

	let authed = $state(null);
	let entitled = $state(null);

	onMount(async () => {
		try {
			const response = await fetch(`${baseURL}/app/user`, {
				credentials: 'include'
			});
			if (response.ok) {
				authed = true;

				const status = await fetch(`${baseURL}/billing/status/`, {
					credentials: 'include'
				});
				entitled = status.ok ? (await status.json()).entitled : false;
			} else {
				authed = false;
				goto('/login');
			}
		} catch {
			authed = false;
			goto('/login');
		}
	});

	async function logout() {
		await fetch(`${baseURL}/app/logout/`, {
			method: 'POST',
			credentials: 'include'
		});
		goto('/login');
	}
</script>

{#if authed === null || entitled === null}
	<div class="min-h-screen bg-base-100 flex items-center justify-center">
		<span class="loading loading-spinner loading-lg"></span>
	</div>
{:else if !entitled}
	<div class="min-h-screen bg-base-100 flex items-center justify-center p-4">
		<div class="card bg-base-200 border-4 border-base-300 w-full max-w-md">
			<div class="card-body items-center text-center gap-4">
				<h1 class="card-title text-2xl">Subscription required</h1>
				<p>Readablock requires an active subscription to keep reading. Choose a plan to continue.</p>
				<a href="/#pricing" class="btn btn-primary">View plans</a>
				<button onclick={logout} class="btn btn-ghost">Log out</button>
			</div>
		</div>
	</div>
{:else if authed}
	{#if !$page.url.pathname.startsWith('/read')}
		<Navbar />
	{/if}

	<slot />
{/if}
