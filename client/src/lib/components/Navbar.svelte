<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { baseURL, selectedLanguage } from '$lib/state.svelte.js';
	import { Library, Upload, Languages, LogOut } from 'lucide-svelte';

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
	}

	async function logout() {
		await fetch(`${baseURL}/app/logout/`, {
			method: 'POST',
			credentials: 'include'
		});
		goto('/login');
	}

	function currentLanguageName() {
		if (!selectedLanguage.value) return 'Language';
		const lang = languages.find((l) => l.deepl === selectedLanguage.value);
		return lang ? lang.name : 'Language';
	}
</script>

<div class="navbar bg-base-200 border-b border-base-300">
	<div class="navbar-start">
		<button
			onclick={() => goto('/dashboard')}
			class="font-display text-2xl font-bold text-primary btn btn-ghost btn-lg">Readablock</button
		>

		<div class="dropdown dropdown-end">
			<div tabindex="0" role="button" class="btn btn-ghost gap-2">
				<Languages class="h-4 w-4" />
				{currentLanguageName()}
			</div>
			<div
				tabindex="0"
				class="dropdown-content list bg-base-200 rounded-box z-1 w-52 overflow-y-auto max-h-64 shadow-sm"
			>
				{#each languages as lang}
					<div
						class="list-row cursor-pointer hover:bg-base-300"
						class:bg-base-300={selectedLanguage.value === lang.deepl}
						onclick={() => selectLanguage(lang.deepl)}
					>
						{lang.name}
					</div>
				{/each}
			</div>
		</div>
	</div>

	<div class="navbar-center">
		<ul class="menu menu-horizontal px-1 gap-1">
			<li>
				<button
					onclick={() => goto('/dashboard')}
					class="gap-2 btn"
					class:active={$page.url.pathname === '/dashboard'}
				>
					<Library class="h-4 w-4" />
					Dashboard
				</button>
			</li>
			<li>
				<button
					onclick={() => goto('/upload')}
					class="gap-2 btn"
					class:active={$page.url.pathname === '/upload'}
				>
					<Upload class="h-4 w-4" />
					Upload
				</button>
			</li>
		</ul>
	</div>

	<div class="navbar-end gap-1">
		<button class="btn btn-ghost" onclick={logout}>
			<LogOut class="h-4 w-4" />
		</button>
	</div>
</div>
