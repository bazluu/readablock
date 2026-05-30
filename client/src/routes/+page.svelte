<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { BookOpen, Target, Puzzle, Check, ArrowDown } from 'lucide-svelte';

	let selectedWord = $state('');
	let translation = $state('');
	let hoveredFeature = $state(null);

	const italianExcerpt = [
		{ text: "C'era", translation: 'There was' },
		{ text: 'una', translation: 'a/an' },
		{ text: 'volta...', translation: 'once...' },
		{ text: '—Un', translation: '—A' },
		{ text: 'pezzo', translation: 'piece' },
		{ text: 'di', translation: 'of' },
		{ text: 'legno.', translation: 'wood.' },
		{ text: 'Non', translation: 'Not' },
		{ text: 'era', translation: 'was' },
		{ text: 'un', translation: 'a' },
		{ text: 'legno', translation: 'wood' },
		{ text: 'di', translation: 'of' },
		{ text: 'lusso,', translation: 'luxury,' },
		{ text: 'ma', translation: 'but' },
		{ text: 'un', translation: 'a' },
		{ text: 'semplice', translation: 'simple' },
		{ text: 'pezzo', translation: 'piece' },
		{ text: 'da', translation: 'from' },
		{ text: 'catasta,', translation: 'woodpile,' },
		{ text: 'di', translation: 'of' },
		{ text: 'quelli', translation: 'those' },
		{ text: 'che', translation: 'that' },
		{ text: "d'inverno", translation: 'in winter' },
		{ text: 'si', translation: 'one' },
		{ text: 'mettono', translation: 'puts' },
		{ text: 'nelle', translation: 'in the' },
		{ text: 'stufe', translation: 'stoves' },
		{ text: 'e', translation: 'and' },
		{ text: 'nei', translation: 'in the' },
		{ text: 'caminetti', translation: 'fireplaces' },
		{ text: 'per', translation: 'to' },
		{ text: 'accendere', translation: 'light' },
		{ text: 'il', translation: 'the' },
		{ text: 'fuoco', translation: 'fire' },
		{ text: 'e', translation: 'and' },
		{ text: 'per', translation: 'to' },
		{ text: 'riscaldare', translation: 'warm' },
		{ text: 'le', translation: 'the' },
		{ text: 'stanze.', translation: 'rooms.' }
	];

	const features = [
		{
			title: 'Immersive Reading',
			description:
				'Read authentic literature in your target language. Every word is a lesson waiting to be discovered.',
			icon: BookOpen
		},
		{
			title: 'Contextual Learning',
			description:
				'Click any word or sentence for instant translation. Learn vocabulary in the context of real stories, not isolated lists.',
			icon: Target
		},
		{
			title: 'Chunking Mastery',
			description:
				"Reinforce learning through our sentence reorganization game. Practice the phrases and patterns you've read.",
			icon: Puzzle
		}
	];

	const pricingPlans = [
		{
			name: 'Reader',
			price: '$6',
			period: 'per month',
			features: [
				'Full library access',
				'Unlimited translations',
				'Unlimited games',
				'Sentence analysis',
				'Progress tracking',
				'Priority support'
			],
			cta: 'Begin Your Journey',
			highlighted: false
		}
		// {
		// 	name: 'Polyglot',
		// 	price: '$99',
		// 	period: 'per year',
		// 	features: [
		// 		'Everything in Reader',
		// 		'Multiple languages',
		// 		'Custom book uploads',
		// 		'Advanced analytics',
		// 		'Offline mode',
		// 		'Early access features'
		// 	],
		// 	cta: 'Master Languages',
		// 	highlighted: false
		// }
	];

	function handleWordClick(word, trans) {
		selectedWord = word;
		translation = trans;
		setTimeout(() => {
			selectedWord = '';
			translation = '';
		}, 2000);
	}

	let scrollY = $state(0);

	onMount(() => {
		const handleScroll = () => {
			scrollY = window.scrollY;
		};
		window.addEventListener('scroll', handleScroll);
		return () => {
			window.removeEventListener('scroll', handleScroll);
		};
	});
</script>

<svelte:head>
	<title>readablock — Learn Languages Through Immersion</title>
</svelte:head>

<div class="w-full min-h-screen bg-base-100 text-base-content font-serif overflow-x-hidden">
	<!-- Hero Section -->
	<section class="hero min-h-screen border-b-4 border-base-300">
		<div class="hero-content flex-col lg:flex-row gap-12 max-w-7xl w-full py-16">
			<div class="flex-1 space-y-8">
				<h1
					class="font-display text-6xl md:text-7xl lg:text-8xl font-bold leading-none tracking-tight"
				>
					Read.<br />
					Click.<br />
					<span class="text-primary">Learn.</span>
				</h1>
				<p class="text-xl md:text-2xl text-base-content/60 max-w-lg leading-relaxed">
					Master languages through immersive reading.<br />Every word tells a story.<br />Every
					sentence builds fluency.
				</p>
				<div class="flex gap-4 flex-wrap">
					<button onclick={() => goto('/dashboard')} class="btn btn-primary btn-xl text-xl px-12"
						>Start Reading</button
					>
				</div>
			</div>

			<div class="flex-1 relative max-w-lg">
				<div
					class="card bg-base-200 border-4 border-base-300 shadow-2xl transition-transform duration-300 hover:scale-[1.02]"
					style="transform: perspective(1000px) rotateY(-5deg);"
				>
					<div class="card-body p-8">
						<div class="flex justify-between items-center pb-6 border-b-2 border-base-300 mb-8">
							<span class="font-display text-xl md:text-2xl font-bold italic"
								>Le Avventure di Pinocchio</span
							>
							<span class="text-base-content/50 text-sm">Chapter 1</span>
						</div>
						<div class="relative min-h-[300px]">
							<p class="text-xl md:text-2xl leading-loose">
								{#each italianExcerpt as word, i}
									<button
										class="bg-transparent border-0 text-base-content cursor-pointer px-0.5 py-0.5 transition-all duration-200 relative hover:text-primary inline-block animate-fadeInWord {selectedWord ===
										word.text
											? 'text-primary font-semibold'
											: ''}"
										style="animation-delay: {i * 0.05}s"
										onclick={() => handleWordClick(word.text, word.translation)}
									>
										{word.text}
									</button>
								{/each}
							</p>
							{#if translation}
								<div
									class="absolute bottom-full left-1/2 -translate-x-1/2 bg-base-300 border-2 border-primary px-6 py-4 rounded-lg flex flex-col gap-2 animate-tooltipAppear shadow-2xl"
								>
									<span class="text-xl font-bold text-primary">{selectedWord}</span>
									<span class="text-base text-base-content/60">{translation}</span>
								</div>
							{/if}
						</div>
					</div>
				</div>
			</div>
		</div>

		<div
			class="absolute bottom-12 flex flex-col items-center gap-4 text-base-content/50 text-sm tracking-widest uppercase"
		>
			<ArrowDown class="w-4 h-4 animate-bounce" />
			<span>Scroll</span>
		</div>
	</section>

	<!-- Features Section -->
	<section class="py-40 px-8 border-b-4 border-base-300">
		<div class="text-center max-w-4xl mx-auto mb-24">
			<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
				The Science of Language Immersion
			</h2>
			<p class="text-2xl text-base-content/60">Three principles. Infinite possibilities.</p>
		</div>

		<div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
			{#each features as feature, i}
				{@const Icon = feature.icon}
				<div
					class="card bg-base-200 border-4 border-base-300 transition-all duration-300 hover:-translate-y-3 hover:border-primary animate-fadeInUp relative overflow-hidden"
					style="animation-delay: {i * 0.2}s"
					onmouseenter={() => (hoveredFeature = i)}
					onmouseleave={() => (hoveredFeature = null)}
				>
					<div class="card-body p-12">
						<Icon class="h-12 w-12 text-primary mb-4" />
						<h3 class="font-display text-3xl font-bold mb-4">{feature.title}</h3>
						<p class="text-base-content/60 text-lg leading-relaxed">{feature.description}</p>
					</div>
					<div
						class="absolute bottom-0 left-0 right-0 h-1 bg-primary scale-x-0 transition-transform duration-300 origin-left {hoveredFeature ===
						i
							? 'scale-x-100'
							: ''}"
					></div>
				</div>
			{/each}
		</div>
	</section>

	<!-- How It Works -->
	<section class="py-40 px-8 bg-base-200 border-b-4 border-base-300">
		<div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-24 items-start">
			<div>
				<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold leading-none mb-8">
					From Pages<br />to Fluency
				</h2>
				<p class="text-2xl text-base-content/60 mb-16 leading-relaxed">
					readablock transforms classic literature into your personal language laboratory. Read
					authentic texts, build vocabulary in context, and reinforce learning through play.
				</p>
				<div class="stats stats-vertical md:stats-horizontal shadow">
					<div class="stat">
						<div class="stat-value text-primary">10,000+</div>
						<div class="stat-title">Words Learned</div>
					</div>
					<div class="stat">
						<div class="stat-value text-primary">500+</div>
						<div class="stat-title">Books Available</div>
					</div>
					<div class="stat">
						<div class="stat-value text-primary">12</div>
						<div class="stat-title">Languages</div>
					</div>
				</div>
			</div>

			<div class="flex flex-col gap-12">
				{#each [{ num: '01', title: 'Choose Your Book', desc: 'Select from classics like Pinocchio, Don Quixote, or contemporary novels.' }, { num: '02', title: 'Read & Discover', desc: 'Click any word or sentence for instant translation and context.' }, { num: '03', title: 'Practice Chunking', desc: 'Reorganize sentences from your reading to master sentence patterns.' }, { num: '04', title: 'Track Progress', desc: 'Watch your vocabulary grow and fluency improve over time.' }] as step}
					<div class="grid grid-cols-[auto_1fr] gap-8 items-start">
						<div class="font-display text-6xl font-bold leading-none text-base-content/20">
							{step.num}
						</div>
						<div>
							<h4 class="font-display text-3xl font-bold mb-3">{step.title}</h4>
							<p class="text-base-content/60 text-lg">{step.desc}</p>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- Pricing Section -->
	<section class="py-40 px-8 border-b-4 border-base-300">
		<div class="text-center max-w-4xl mx-auto mb-24">
			<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
				Choose Your Path
			</h2>
			<p class="text-2xl text-base-content/60">
				Start free. Upgrade when you're ready to master more.
			</p>
		</div>

		<div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each pricingPlans as plan, i}
				<div
					class="card bg-base-200 border-4 transition-all duration-300 hover:-translate-y-3 animate-fadeInUp {plan.highlighted
						? 'border-primary scale-105'
						: 'border-base-300'}"
					style="animation-delay: {i * 0.15}s"
				>
					<div class="card-body p-12">
						{#if plan.highlighted}
							<div class="absolute -top-3 left-1/2 -translate-x-1/2">
								<span class="badge badge-primary badge-lg font-bold uppercase tracking-wider">
									Most Popular
								</span>
							</div>
						{/if}
						<h3 class="font-display text-3xl font-bold mb-6">{plan.name}</h3>
						<div class="flex items-baseline gap-2 mb-8 pb-8 border-b-2 border-base-300">
							<span class="font-display text-6xl font-bold leading-none">{plan.price}</span>
							<span class="text-base-content/50 text-lg">{plan.period}</span>
						</div>
						<ul class="mb-10 flex flex-col gap-4">
							{#each plan.features as feature}
								<li class="flex items-center gap-3 text-lg text-base-content/60">
									<Check class="w-5 h-5 text-primary shrink-0" />
									{feature}
								</li>
							{/each}
						</ul>
						<button class="btn {plan.highlighted ? 'btn-primary' : 'btn-outline'} btn-lg w-full">
							{plan.cta}
						</button>
					</div>
				</div>
			{/each}
		</div>
	</section>

	<!-- CTA Section -->
	<section class="hero py-40 px-8 border-b-4 border-base-300">
		<div class="hero-content text-center max-w-4xl">
			<div class="flex flex-col items-center">
				<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
					Begin Your Language Journey Today
				</h2>
				<p class="text-2xl text-base-content/60 mb-12">
					Join our learners discovering the joy of reading in a new language.
				</p>
				<button onclick={() => goto('/dashboard')} class="btn btn-primary btn-xl text-xl px-12"
					>Start Reading</button
				>
			</div>
		</div>
	</section>

	<!-- Footer -->
	<footer class="footer p-10 bg-base-200 text-base-content">
		<aside class="flex-1">
			<h3 class="font-display text-4xl font-bold mb-2">readablock</h3>
			<p class="text-base-content/50 text-lg">Language immersion through literature</p>
		</aside>
		<nav class="flex-1 grid grid-cols-1 sm:grid-cols-3 gap-12">
			<div>
				<h4 class="font-display text-lg font-bold mb-4 footer-title">Product</h4>
				<a href="#features" class="link link-hover">Features</a>
				<a href="#pricing" class="link link-hover">Pricing</a>
				<a href="#languages" class="link link-hover">Languages</a>
			</div>
			<div>
				<h4 class="font-display text-lg font-bold mb-4 footer-title">Resources</h4>
				<a href="#github" class="link link-hover">GitHub</a>
				<a href="#guides" class="link link-hover">Learning Guides</a>
				<a href="#research" class="link link-hover">Research</a>
				<a href="#faq" class="link link-hover">FAQ</a>
			</div>
			<div>
				<h4 class="font-display text-lg font-bold mb-4 footer-title">Company</h4>
				<a href="#about" class="link link-hover">About</a>
				<a href="#contact" class="link link-hover">Contact</a>
				<a href="#privacy" class="link link-hover">Privacy</a>
				<a href="#terms" class="link link-hover">Terms</a>
			</div>
		</nav>
	</footer>
	<div class="footer-center p-4 bg-base-200 text-base-content/50 text-center text-base">
		<p>&copy; 2026 readablock. All rights reserved.</p>
	</div>
</div>

<style>
	@keyframes fadeInWord {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.animate-fadeInWord {
		animation: fadeInWord 0.6s ease backwards;
	}

	@keyframes tooltipAppear {
		from {
			opacity: 0;
			transform: translateX(-50%) translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateX(-50%) translateY(0);
		}
	}

	.animate-tooltipAppear {
		animation: tooltipAppear 0.3s ease;
	}

	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(40px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.animate-fadeInUp {
		animation: fadeInUp 0.8s ease backwards;
	}
</style>
