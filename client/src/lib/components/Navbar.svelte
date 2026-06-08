<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { baseURL, selectedLanguage } from '$lib/state.svelte.js';
	import { Library, Upload, Languages, MessageSquare, LogOut } from 'lucide-svelte';

	let languages = $state([]);
	let langDropdownOpen = $state(false);

	onMount(async () => {
		const response = await fetch(`${baseURL}/app/supported-languages`, {
			credentials: 'include'
		});
		if (response.ok) {
			const data = await response.json();
			languages = data.languages;
		}
	});

	function clickOutside(node, callback) {
		const handleClick = (event) => {
			if (!node.contains(event.target)) {
				callback();
			}
		};
		document.addEventListener('click', handleClick, true);
		return {
			destroy() {
				document.removeEventListener('click', handleClick, true);
			}
		};
	}

	function selectLanguage(deepl) {
		selectedLanguage.value = deepl;
		langDropdownOpen = false;
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

<div
	class="flex items-center py-1 sm:py-2 bg-base-200 border-b border-base-300 text-neutral-100 gap-1 sm:gap-2"
>
	<div class="flex items-center flex-1 gap-1 sm:gap-2">
		<button
			onclick={() => goto('/dashboard')}
			class="btn font-display text-base sm:text-2xl font-bold text-primary transition-colors"
		>
			Readablock
		</button>

		<div class="relative shrink-0" use:clickOutside={() => (langDropdownOpen = false)}>
			<button
				onclick={() => (langDropdownOpen = !langDropdownOpen)}
				class="btn inline-flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg"
			>
				<Languages class="h-3.5 w-3.5 sm:h-4 sm:w-4" />
				<span class="hidden sm:inline">{currentLanguageName()}</span>
			</button>
			{#if langDropdownOpen}
				<div
					class="absolute top-full left-0 mt-1 bg-base-200 border border-base-300 rounded-lg shadow-lg z-50 w-52 overflow-y-auto max-h-64"
				>
					{#each languages as lang}
						<button
							class="w-full text-left px-4 py-2 btn {selectedLanguage.value === lang.deepl
								? 'btn-neutral'
								: ''}"
							onclick={() => selectLanguage(lang.deepl)}
						>
							{lang.name}
						</button>
					{/each}
				</div>
			{/if}
		</div>
	</div>

	<div class="flex items-center justify-center">
		<div class="flex gap-0.5 sm:gap-1">
			<button
				onclick={() => goto('/dashboard')}
				class="btn inline-flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1.5 sm:py-2 rounded-lg {$page
					.url.pathname === '/dashboard'
					? 'btn-neutral'
					: ''}"
			>
				<Library class="h-3.5 w-3.5 sm:h-4 sm:w-4" />
				<span class="hidden sm:inline">Dashboard</span>
			</button>
			<button
				onclick={() => goto('/upload')}
				class="btn inline-flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1.5 sm:py-2 rounded-lg {$page
					.url.pathname === '/upload'
					? 'btn-neutral'
					: ''}"
			>
				<Upload class="h-3.5 w-3.5 sm:h-4 sm:w-4" />
				<span class="hidden sm:inline">Upload</span>
			</button>
			<button
				onclick={() => goto('/feedback')}
				class="btn inline-flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1.5 sm:py-2 rounded-lg {$page
					.url.pathname === '/feedback'
					? 'btn-neutral'
					: ''}"
			>
				<MessageSquare class="h-3.5 w-3.5 sm:h-4 sm:w-4" />
				<span class="hidden sm:inline">Feedback</span>
			</button>
		</div>
	</div>

	<div class="flex items-center justify-end flex-1 gap-1 min-w-0">
		<button
			class="btn inline-flex items-center justify-center p-1.5 sm:p-2 transition-colors shrink-0"
			onclick={logout}
		>
			<LogOut class="h-3.5 w-3.5 sm:h-4 sm:w-4" />
		</button>
	</div>
</div>
