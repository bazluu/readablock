<script>
	import { Book, BookCheck, BookOpen, MoreVertical } from 'lucide-svelte';

	let { book, onopen, onunread, ondownload } = $props();

	let percent = $derived(
		book.sentence_count ? Math.round((book.sentence_last_read / book.sentence_count) * 100) : 0
	);
	let state = $derived(percent >= 100 ? 'completed' : percent > 0 ? 'in-progress' : 'unread');

	let accent = $derived(
		{
			completed: {
				border: 'hover:border-success',
				icon: 'text-success'
			},
			'in-progress': {
				border: 'hover:border-primary',
				icon: 'text-primary'
			},
			unread: {
				border: 'hover:border-secondary',
				icon: 'text-secondary'
			}
		}[state]
	);
</script>

<div
	class="card box-border w-full min-h-56 overflow-hidden bg-base-200 border border-base-300 {accent.border} hover:shadow-lg transition-all duration-200 text-left p-4"
>
	<div class="flex flex-1 flex-row gap-4">
		<div
			class="relative w-1/2 shrink-0 self-stretch bg-base-300 rounded-lg flex items-center justify-center overflow-hidden"
		>
			{#if state === 'completed'}
				<BookCheck class="h-12 w-12 {accent.icon}" />
			{:else if state === 'in-progress'}
				<BookOpen class="h-12 w-12 {accent.icon}" />
			{:else}
				<Book class="h-12 w-12 {accent.icon}" />
			{/if}
		</div>
		<div class="flex flex-col gap-3 min-w-0 flex-1">
			<div class="flex flex-col gap-1">
				<p class="font-bold text-base leading-tight line-clamp-2">
					{book.title_en || book.title}
				</p>
				{#if book.title_en && book.title}
					<p class="-mt-0.5 font-serif text-sm text-base-content/60 leading-tight line-clamp-2">
						{book.title}
					</p>
				{/if}
				<p class="text-sm font-medium text-base-content/50 leading-tight line-clamp-1">
					{book.author}
				</p>
			</div>
			<div class="flex flex-col gap-2 mt-auto pt-3 border-t border-base-300">
				{#if state !== 'unread'}
					<div class="flex flex-row items-center gap-3">
						<progress
							class="progress progress-primary flex-1 h-1.5"
							value={book.sentence_last_read}
							max={book.sentence_count || 1}
						></progress>
						<span class="text-xs font-bold {accent.icon}">{percent}%</span>
					</div>
				{/if}
				<div class="flex flex-row items-center gap-2">
		<button
			class="btn btn-sm flex-1 {state === 'unread' ? 'btn-secondary' : 'btn-primary'}"
			onclick={() => onopen(book.id)}
		>
			<BookOpen class="h-4 w-4" /> Read
		</button>
		<div class="dropdown dropdown-top dropdown-end">
			<div role="button" tabindex="0" class="btn btn-sm btn-ghost btn-circle">
				<MoreVertical class="h-4 w-4" />
			</div>
			<ul
				tabindex="0"
				class="dropdown-content menu bg-base-100 rounded-box z-10 w-40 p-2 shadow-lg border border-base-300"
			>
				<li>
					<button
						class="w-full bg-transparent border-0 text-left cursor-pointer hover:bg-base-300"
						disabled={state === 'unread'}
						onclick={() => onunread?.(book.id)}
					>
						Mark as unread
					</button>
				</li>
				{#if book.is_owner}
					<li><button class="w-full bg-transparent border-0 text-left cursor-pointer hover:bg-base-300" onclick={() => ondownload?.(book.id)}>Download</button></li>
					<li>
						<button class="w-full bg-transparent border-0 text-left cursor-pointer text-error hover:bg-base-300">
							Delete
						</button>
					</li>
				{/if}
			</ul>
		</div>
		</div>
	</div>
		</div>
	</div>
</div>
