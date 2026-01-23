<script>
	const baseURL = 'http://127.0.0.1:8000';

	let isLogin = true;

	let loginData = {
		email: '',
		password: ''
	};

	let signupData = {
		email: '',
		password: '',
		confirmPassword: ''
	};

	let errorMessage = '';
	let successMessage = '';
	let isLoading = false;

	function toggleForm() {
		isLogin = !isLogin;
		errorMessage = '';
		successMessage = '';
	}

	async function handleLogin(e) {
		e.preventDefault();
		errorMessage = '';
		successMessage = '';
		isLoading = true;

		try {
			const response = await fetch(`${baseURL}/app/login/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				credentials: 'include',
				body: JSON.stringify({
					email: loginData.email,
					password: loginData.password
				})
			});

			const data = await response.json();

			if (response.ok) {
				successMessage = data.message;
				setTimeout(() => {
					window.location.href = '/read';
				}, 1000);
			} else {
				errorMessage = data.message;
			}
		} catch (error) {
			console.error('Login error:', error);
			errorMessage = 'An error occurred during login. Please try again.';
		} finally {
			isLoading = false;
		}
	}

	async function handleSignup(e) {
		e.preventDefault();
		errorMessage = '';
		successMessage = '';

		if (signupData.password !== signupData.confirmPassword) {
			errorMessage = 'Passwords do not match!';
			return;
		}

		isLoading = true;

		try {
			const response = await fetch(`${baseURL}/app/signup/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				credentials: 'include',
				body: JSON.stringify({
					email: signupData.email,
					password: signupData.password
				})
			});

			const data = await response.json();

			if (response.ok) {
				successMessage = data.message;
				setTimeout(() => {
					window.location.href = '/read';
				}, 1000);
			} else {
				errorMessage = data.message;
			}
		} catch (error) {
			console.error('Signup error:', error);
			errorMessage = 'An error occurred during signup. Please try again.';
		} finally {
			isLoading = false;
		}
	}
</script>

<div
	class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/20 via-base-100 to-secondary/20 p-4 overflow-x-hidden"
>
	<div class="card w-full max-w-md bg-base-100 shadow-2xl">
		<div class="card-body p-6 sm:p-8">
			<!-- Header -->
			<div class="text-center mb-6">
				<h2 class="text-3xl font-bold text-primary mb-2">
					{isLogin ? 'Welcome Back' : 'Create Account'}
				</h2>
				<p class="text-base-content/60">
					{isLogin ? 'Sign in to continue' : 'Sign up to get started'}
				</p>
			</div>

			<!-- Error/Success Messages -->
			{#if errorMessage}
				<div class="alert alert-error mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="stroke-current shrink-0 h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<span>{errorMessage}</span>
				</div>
			{/if}

			{#if successMessage}
				<div class="alert alert-success mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="stroke-current shrink-0 h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
					<span>{successMessage}</span>
				</div>
			{/if}

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
							disabled={isLoading}
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
							disabled={isLoading}
							required
						/>
						<div class="w-full text-right">
							<a href="#" class="underline text-base-content/60 m-0">Forgot password?</a>
						</div>
					</div>

					<div class="form-control mt-6">
						<button type="submit" class="btn btn-primary w-full" disabled={isLoading}>
							{#if isLoading}
								<span class="loading loading-spinner"></span>
								Signing in...
							{:else}
								Sign In
							{/if}
						</button>
					</div>
				</form>
			{:else}
				<!-- Signup Form -->
				<form on:submit={handleSignup} class="space-y-4">
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
							disabled={isLoading}
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
							disabled={isLoading}
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
							disabled={isLoading}
							required
						/>
					</div>

					<div class="form-control">
						<label class="label cursor-pointer justify-start gap-2">
							<input
								type="checkbox"
								class="checkbox checkbox-primary"
								disabled={isLoading}
								required
							/>
							<span class="label-text"
								>I agree to the <a href="#" class="link link-primary">terms and conditions</a></span
							>
						</label>
					</div>

					<div class="form-control mt-6">
						<button type="submit" class="btn btn-primary w-full" disabled={isLoading}>
							{#if isLoading}
								<span class="loading loading-spinner"></span>
								Creating Account...
							{:else}
								Create Account
							{/if}
						</button>
					</div>
				</form>
			{/if}

			<!-- Toggle Form -->
			<div class="text-center mt-6">
				<p class="text-sm text-base-content/60">
					{isLogin ? "Don't have an account?" : 'Already have an account?'}
					<button
						on:click={toggleForm}
						class="btn btn-sm btn-outline text-base-content/60 font-semibold ml-1"
						disabled={isLoading}
					>
						{isLogin ? 'Sign up' : 'Sign in'}
					</button>
				</p>
			</div>
		</div>
	</div>
</div>

<style>
	:global(*) {
		box-sizing: border-box;
	}

	:global(body) {
		margin: 0;
		padding: 0;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
	}
</style>
