<script>
	import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';
	import { CheckCircleSolid } from 'flowbite-svelte-icons';
</script>

<Navbar>
	<NavBrand href="/">
		<CheckCircleSolid />
		<span class="m-5 self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			Another To Do App
		</span>
	</NavBrand>
	<NavHamburger />
	<NavUl>
		<NavLi href="/">Home</NavLi>
		<NavLi href="/dashboard">Dashboard</NavLi>
	</NavUl>
</Navbar>
