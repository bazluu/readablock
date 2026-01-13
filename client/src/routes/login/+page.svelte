<script>
	let isLogin = true;

	let loginData = {
		email: '',
		password: ''
	};

	let signupData = {
		name: '',
		email: '',
		password: '',
		confirmPassword: ''
	};

	function toggleForm() {
		isLogin = !isLogin;
	}

	function handleLogin(e) {
		e.preventDefault();
		console.log('Login:', loginData);
		// Add your login logic here
	}

	function handleSignup(e) {
		e.preventDefault();
		if (signupData.password !== signupData.confirmPassword) {
			alert('Passwords do not match!');
			return;
		}
		console.log('Signup:', signupData);
		// Add your signup logic here
	}
</script>

<div
	class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/20 via-base-100 to-secondary/20 p-4"
>
	<div class="card w-full max-w-md bg-base-100 shadow-2xl">
		<div class="card-body p-4">
			<!-- Header -->
			<div class="text-center mb-6">
				<h2 class="text-3xl font-bold text-primary mb-2">
					{isLogin ? 'Welcome Back' : 'Create Account'}
				</h2>
				<p class="text-base-content/60">
					{isLogin ? 'Sign in to continue' : 'Sign up to get started'}
				</p>
			</div>

			{#if isLogin}
				<!-- Login Form -->
				<form on:submit={handleLogin} class="space-y-4">
					<div class="form-control">
						<label class="label" for="login-email">
							<span class="label-text">Email</span>
						</label>
						<input
							id="login-email"
							type="email"
							placeholder="your@email.com"
							class="input input-bordered w-full"
							bind:value={loginData.email}
							required
						/>
					</div>

					<div class="form-control">
						<label class="label" for="login-password">
							<span class="label-text">Password</span>
						</label>
						<input
							id="login-password"
							type="password"
							placeholder="••••••••"
							class="input input-bordered w-full"
							bind:value={loginData.password}
							required
						/>
						<label class="label">
							<a href="#" class="label-text-alt link link-hover text-primary">Forgot password?</a>
						</label>
					</div>

					<div class="form-control mt-6">
						<button type="submit" class="btn btn-primary w-full"> Sign In </button>
					</div>
				</form>
			{:else}
				<!-- Signup Form -->
				<form on:submit={handleSignup} class="space-y-4">
					<div class="form-control">
						<label class="label" for="signup-name">
							<span class="label-text">Full Name</span>
						</label>
						<input
							id="signup-name"
							type="text"
							placeholder="John Doe"
							class="input input-bordered w-full"
							bind:value={signupData.name}
							required
						/>
					</div>

					<div class="form-control">
						<label class="label" for="signup-email">
							<span class="label-text">Email</span>
						</label>
						<input
							id="signup-email"
							type="email"
							placeholder="your@email.com"
							class="input input-bordered w-full"
							bind:value={signupData.email}
							required
						/>
					</div>

					<div class="form-control">
						<label class="label" for="signup-password">
							<span class="label-text">Password</span>
						</label>
						<input
							id="signup-password"
							type="password"
							placeholder="••••••••"
							class="input input-bordered w-full"
							bind:value={signupData.password}
							required
						/>
					</div>

					<div class="form-control">
						<label class="label" for="signup-confirm">
							<span class="label-text">Confirm Password</span>
						</label>
						<input
							id="signup-confirm"
							type="password"
							placeholder="••••••••"
							class="input input-bordered w-full"
							bind:value={signupData.confirmPassword}
							required
						/>
					</div>

					<div class="form-control">
						<label class="label cursor-pointer justify-start gap-2">
							<input type="checkbox" class="checkbox checkbox-primary" required />
							<span class="label-text"
								>I agree to the <a href="#" class="link link-primary">terms and conditions</a></span
							>
						</label>
					</div>

					<div class="form-control mt-6">
						<button type="submit" class="btn btn-primary w-full"> Create Account </button>
					</div>
				</form>
			{/if}

			<!-- Toggle Form -->
			<div class="text-center mt-6">
				<p class="text-sm text-base-content/60">
					{isLogin ? "Don't have an account?" : 'Already have an account?'}
					<button type="button" on:click={toggleForm} class="link link-primary font-semibold ml-1">
						{isLogin ? 'Sign up' : 'Sign in'}
					</button>
				</p>
			</div>
		</div>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
	}
</style>
