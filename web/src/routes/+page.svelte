<script lang='ts'>

	import Navbar from './navbar.svelte';

	import { onMount } from 'svelte';
	import TodoTable from '../components/todo_table.svelte';
	import { loadTags, loadTodos } from '../store';

	onMount(async () => {await loadTodos(); await loadTags()});

</script>

<Navbar></Navbar>

<div class="main-div">
	<TodoTable/>
</div>
