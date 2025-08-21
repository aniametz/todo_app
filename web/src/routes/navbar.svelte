<script>
	import { page } from '$app/state';
	import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';
	import { BadgeCheckOutline } from 'flowbite-svelte-icons';

	let activeUrl = $derived(page.url.pathname);
</script>

<Navbar class="sticky top-0 z-40 mx-auto w-full flex-none border-b border-gray-200 bg-white dark:border-gray-600 dark:bg-gray-900">
	<NavBrand href="/">
		<BadgeCheckOutline class="text-blue-600 dark:text-blue-400" size="lg"/>
		<span class="m-5 self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			Another To Do App
		</span>
	</NavBrand>
	<NavHamburger />
	<NavUl {activeUrl}>
		<NavLi href="/">Home</NavLi>
		<NavLi href="/manage_tags">Manage Tags</NavLi>
		<NavLi href="/archived_todos">Archived Todos</NavLi>
		<NavLi href="/dashboard">Dashboard</NavLi>
	</NavUl>
</Navbar>
