<script>
	import { onMount } from 'svelte';

	let selectedWord = '';
	let translation = '';
	let hoveredFeature = null;

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
			icon: '📖'
		},
		{
			title: 'Contextual Learning',
			description:
				'Click any word or sentence for instant translation. Learn vocabulary in the context of real stories, not isolated lists.',
			icon: '🎯'
		},
		{
			title: 'Chunking Mastery',
			description:
				"Reinforce learning through our sentence reorganization game. Practice the phrases and patterns you've read.",
			icon: '🧩'
		}
	];

	const pricingPlans = [
		{
			name: 'Free',
			price: '$0',
			period: 'forever',
			features: [
				'3 books available',
				'Basic word translations',
				'50 games per month',
				'Community support'
			],
			cta: 'Start Reading',
			highlighted: false
		},
		{
			name: 'Reader',
			price: '$12',
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
			highlighted: true
		},
		{
			name: 'Polyglot',
			price: '$99',
			period: 'per year',
			features: [
				'Everything in Reader',
				'Multiple languages',
				'Custom book uploads',
				'Advanced analytics',
				'Offline mode',
				'Early access features'
			],
			cta: 'Master Languages',
			highlighted: false
		}
	];

	function handleWordClick(word, trans) {
		selectedWord = word;
		translation = trans;
		setTimeout(() => {
			selectedWord = '';
			translation = '';
		}, 2000);
	}

	let scrollY = 0;

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
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link
		href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div class="w-full min-h-screen bg-neutral-950 text-neutral-200 font-serif overflow-x-hidden">
	<!-- Hero Section -->
	<section
		class="min-h-screen flex flex-col justify-center items-center px-8 py-16 relative border-b-4 border-neutral-800"
	>
		<div class="max-w-7xl w-full grid grid-cols-1 lg:grid-cols-2 gap-24 items-center">
			<div class="space-y-8">
				<h1
					class="font-display text-6xl md:text-7xl lg:text-8xl font-bold leading-none tracking-tight"
				>
					Read.<br />
					Click.<br />
					<span class="bg-gradient-to-br from-amber-600 to-amber-500 bg-clip-text text-transparent"
						>Learn.</span
					>
				</h1>
				<p class="text-xl md:text-2xl text-neutral-400 max-w-lg leading-relaxed">
					Master languages through immersive reading. Every word tells a story. Every sentence
					builds fluency.
				</p>
				<div class="flex gap-4 flex-wrap">
					<a
						href="/read"
						class="px-10 py-4 bg-amber-600 hover:bg-amber-500 text-neutral-950 font-semibold text-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-amber-600/30 border-2 border-amber-600 tracking-wide"
					>
						Start Reading
					</a>
				</div>
			</div>

			<div class="relative">
				<div
					class="bg-neutral-900 border-4 border-neutral-800 rounded-lg p-8 shadow-2xl transition-transform duration-300 hover:scale-[1.02]"
					style="transform: perspective(1000px) rotateY(-5deg);"
				>
					<div class="flex justify-between items-center pb-6 border-b-2 border-neutral-800 mb-8">
						<span class="font-display text-xl md:text-2xl font-bold italic"
							>Le Avventure di Pinocchio</span
						>
						<span class="text-neutral-500 text-sm">Chapter 1</span>
					</div>
					<div class="relative min-h-[300px]">
						<p class="text-xl md:text-2xl leading-loose">
							{#each italianExcerpt as word, i}
								<button
									class="bg-transparent border-0 text-neutral-200 cursor-pointer px-0.5 py-0.5 transition-all duration-200 relative hover:text-amber-500 inline-block animate-fadeInWord {selectedWord ===
									word.text
										? 'text-amber-600 font-semibold'
										: ''}"
									style="animation-delay: {i * 0.05}s"
									on:click={() => handleWordClick(word.text, word.translation)}
								>
									{word.text}
									<span
										class="absolute bottom-0 left-0 right-0 h-0.5 bg-amber-600 scale-x-0 transition-transform duration-200 origin-left group-hover:scale-x-100"
									></span>
								</button>
							{/each}
						</p>
						{#if translation}
							<div
								class="absolute bottom-full left-1/2 -translate-x-1/2 bg-neutral-800 border-2 border-amber-600 px-6 py-4 rounded-lg flex flex-col gap-2 animate-tooltipAppear shadow-2xl"
							>
								<span class="text-xl font-bold text-amber-500">{selectedWord}</span>
								<span class="text-base text-neutral-400">{translation}</span>
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>

		<div
			class="absolute bottom-12 flex flex-col items-center gap-4 text-neutral-500 text-sm tracking-widest uppercase"
		>
			<div
				class="w-0.5 h-16 bg-gradient-to-b from-transparent via-neutral-800 to-transparent animate-scrollPulse"
			></div>
			<span>Scroll to explore</span>
		</div>
	</section>

	<!-- Features Section -->
	<section class="py-40 px-8 border-b-4 border-neutral-800">
		<div class="text-center max-w-4xl mx-auto mb-24">
			<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
				The Science of Language Immersion
			</h2>
			<p class="text-2xl text-neutral-400">Three principles. Infinite possibilities.</p>
		</div>

		<div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
			{#each features as feature, i}
				<div
					class="bg-neutral-900 border-4 border-neutral-800 p-12 relative transition-all duration-300 hover:-translate-y-3 hover:border-amber-600 animate-fadeInUp"
					style="animation-delay: {i * 0.2}s"
					on:mouseenter={() => (hoveredFeature = i)}
					on:mouseleave={() => (hoveredFeature = null)}
				>
					<div class="text-6xl mb-8">{feature.icon}</div>
					<h3 class="font-display text-3xl font-bold mb-4">{feature.title}</h3>
					<p class="text-neutral-400 text-lg leading-relaxed">{feature.description}</p>
					<div
						class="absolute bottom-0 left-0 right-0 h-1 bg-amber-600 scale-x-0 transition-transform duration-300 origin-left {hoveredFeature ===
						i
							? 'scale-x-100'
							: ''}"
					></div>
				</div>
			{/each}
		</div>
	</section>

	<!-- How It Works -->
	<section class="py-40 px-8 bg-neutral-900 border-b-4 border-neutral-800">
		<div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-24 items-start">
			<div>
				<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold leading-none mb-8">
					From Pages<br />to Fluency
				</h2>
				<p class="text-2xl text-neutral-400 mb-16 leading-relaxed">
					readablock transforms classic literature into your personal language laboratory. Read
					authentic texts, build vocabulary in context, and reinforce learning through play.
				</p>
				<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
					<div class="border-l-4 border-amber-600 pl-6">
						<div class="font-display text-5xl font-bold leading-none mb-2 text-amber-500">
							10,000+
						</div>
						<div class="text-sm text-neutral-500 uppercase tracking-wider">Words Learned</div>
					</div>
					<div class="border-l-4 border-amber-600 pl-6">
						<div class="font-display text-5xl font-bold leading-none mb-2 text-amber-500">500+</div>
						<div class="text-sm text-neutral-500 uppercase tracking-wider">Books Available</div>
					</div>
					<div class="border-l-4 border-amber-600 pl-6">
						<div class="font-display text-5xl font-bold leading-none mb-2 text-amber-500">12</div>
						<div class="text-sm text-neutral-500 uppercase tracking-wider">Languages</div>
					</div>
				</div>
			</div>

			<div class="flex flex-col gap-12">
				<div class="grid grid-cols-[auto_1fr] gap-8 items-start">
					<div class="font-display text-6xl font-bold leading-none text-neutral-600">01</div>
					<div>
						<h4 class="font-display text-3xl font-bold mb-3">Choose Your Book</h4>
						<p class="text-neutral-400 text-lg">
							Select from classics like Pinocchio, Don Quixote, or contemporary novels.
						</p>
					</div>
				</div>
				<div class="grid grid-cols-[auto_1fr] gap-8 items-start">
					<div class="font-display text-6xl font-bold leading-none text-neutral-600">02</div>
					<div>
						<h4 class="font-display text-3xl font-bold mb-3">Read & Discover</h4>
						<p class="text-neutral-400 text-lg">
							Click any word or sentence for instant translation and context.
						</p>
					</div>
				</div>
				<div class="grid grid-cols-[auto_1fr] gap-8 items-start">
					<div class="font-display text-6xl font-bold leading-none text-neutral-600">03</div>
					<div>
						<h4 class="font-display text-3xl font-bold mb-3">Practice Chunking</h4>
						<p class="text-neutral-400 text-lg">
							Reorganize sentences from your reading to master sentence patterns.
						</p>
					</div>
				</div>
				<div class="grid grid-cols-[auto_1fr] gap-8 items-start">
					<div class="font-display text-6xl font-bold leading-none text-neutral-600">04</div>
					<div>
						<h4 class="font-display text-3xl font-bold mb-3">Track Progress</h4>
						<p class="text-neutral-400 text-lg">
							Watch your vocabulary grow and fluency improve over time.
						</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Pricing Section -->
	<section class="py-40 px-8 border-b-4 border-neutral-800">
		<div class="text-center max-w-4xl mx-auto mb-24">
			<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
				Choose Your Path
			</h2>
			<p class="text-2xl text-neutral-400">Start free. Upgrade when you're ready to master more.</p>
		</div>

		<div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each pricingPlans as plan, i}
				<div
					class="bg-neutral-900 border-4 p-12 relative transition-all duration-300 hover:-translate-y-3 animate-fadeInUp {plan.highlighted
						? 'border-amber-600 bg-neutral-800 scale-105'
						: 'border-neutral-800'}"
					style="animation-delay: {i * 0.15}s"
				>
					{#if plan.highlighted}
						<div
							class="absolute -top-3 left-1/2 -translate-x-1/2 bg-amber-600 text-neutral-950 px-6 py-2 text-sm font-bold uppercase tracking-wider"
						>
							Most Popular
						</div>
					{/if}
					<h3 class="font-display text-3xl font-bold mb-6">{plan.name}</h3>
					<div class="flex items-baseline gap-2 mb-8 pb-8 border-b-2 border-neutral-800">
						<span class="font-display text-6xl font-bold leading-none">{plan.price}</span>
						<span class="text-neutral-500 text-lg">{plan.period}</span>
					</div>
					<ul class="mb-10 flex flex-col gap-4">
						{#each plan.features as feature}
							<li class="flex items-center gap-3 text-lg text-neutral-400">
								<svg
									class="w-5 h-5 text-amber-600 flex-shrink-0"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="3"
									stroke-linecap="round"
									stroke-linejoin="round"
								>
									<polyline points="20 6 9 17 4 12"></polyline>
								</svg>
								{feature}
							</li>
						{/each}
					</ul>
					<button
						class="w-full px-10 py-4 font-semibold text-lg transition-all duration-300 border-2 {plan.highlighted
							? 'bg-amber-600 hover:bg-amber-500 text-neutral-950 border-amber-600 hover:-translate-y-1 hover:shadow-2xl hover:shadow-amber-600/30'
							: 'bg-transparent text-neutral-200 border-neutral-800 hover:border-amber-600 hover:text-amber-600'}"
					>
						{plan.cta}
					</button>
				</div>
			{/each}
		</div>
	</section>

	<!-- CTA Section -->
	<section
		class="py-40 px-8 bg-gradient-to-br from-neutral-950 to-neutral-900 border-b-4 border-neutral-800"
	>
		<div class="max-w-4xl mx-auto text-center">
			<h2 class="font-display text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
				Begin Your Language Journey Today
			</h2>
			<p class="text-2xl text-neutral-400 mb-12">
				Join thousands of learners discovering the joy of reading in a new language.
			</p>
			<button
				class="px-12 py-5 bg-amber-600 hover:bg-amber-500 text-neutral-950 font-semibold text-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-amber-600/30 border-2 border-amber-600"
			>
				Start Reading Free
			</button>
			<p class="mt-6 text-neutral-500 text-base">No credit card required • 3 books free forever</p>
		</div>
	</section>

	<!-- Footer -->
	<footer class="pt-24 pb-12 px-8 bg-neutral-900">
		<div
			class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-[1.5fr_2fr] gap-24 pb-16 border-b-2 border-neutral-800"
		>
			<div>
				<h3 class="font-display text-4xl font-bold mb-4">readablock</h3>
				<p class="text-neutral-500 text-lg">Language immersion through literature</p>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-3 gap-12">
				<div>
					<h4 class="font-display text-lg font-bold mb-6">Product</h4>
					<div class="flex flex-col gap-3">
						<a
							href="#features"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200"
							>Features</a
						>
						<a
							href="#pricing"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200"
							>Pricing</a
						>
						<a
							href="#languages"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200"
							>Languages</a
						>
					</div>
				</div>
				<div>
					<h4 class="font-display text-lg font-bold mb-6">Resources</h4>
					<div class="flex flex-col gap-3">
						<a
							href="#github"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200">GitHub</a
						>
						<a
							href="#guides"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200"
							>Learning Guides</a
						>
						<a
							href="#research"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200"
							>Research</a
						>
						<a
							href="#faq"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200">FAQ</a
						>
					</div>
				</div>
				<div>
					<h4 class="font-display text-lg font-bold mb-6">Company</h4>
					<div class="flex flex-col gap-3">
						<a
							href="#about"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200">About</a
						>
						<a
							href="#contact"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200"
							>Contact</a
						>
						<a
							href="#privacy"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200"
							>Privacy</a
						>
						<a
							href="#terms"
							class="text-neutral-400 hover:text-amber-600 transition-colors duration-200">Terms</a
						>
					</div>
				</div>
			</div>
		</div>
		<div class="max-w-7xl mx-auto pt-12 text-center text-neutral-500 text-base">
			<p>&copy; 2026 readablock. All rights reserved.</p>
		</div>
	</footer>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		font-family: 'Crimson Text', Georgia, serif;
		font-size: 18px;
		line-height: 1.7;
	}

	.font-serif {
		font-family: 'Crimson Text', Georgia, serif;
	}

	.font-display {
		font-family: 'Libre Baskerville', Georgia, serif;
	}

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

	@keyframes scrollPulse {
		0%,
		100% {
			opacity: 0.3;
			transform: scaleY(1);
		}
		50% {
			opacity: 1;
			transform: scaleY(1.2);
		}
	}

	.animate-scrollPulse {
		animation: scrollPulse 2s ease-in-out infinite;
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
