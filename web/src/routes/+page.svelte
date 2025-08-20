<script lang='ts'>

	import {
		Accordion,
		AccordionItem
	} from 'flowbite-svelte';
	import Navbar from './navbar.svelte';

	import { onMount } from 'svelte';
	import TagsTable from '../components/tags_table.svelte';
	import TodoArchivedTable from '../components/todo_archived_table.svelte';
	import TodoTable from '../components/todo_table.svelte';
	import { loadTags, loadTodos } from '../store';

	onMount(async () => {await loadTodos(); await loadTags()});

</script>

<Navbar></Navbar>

<div class="text-center">
	<Accordion>
		<AccordionItem open>
			<span slot="header">Current To Dos</span>
			<TodoTable/>
		</AccordionItem>

		<AccordionItem>
			<span slot="header">Manage Tags</span>
			<TagsTable/>
		</AccordionItem>

		<AccordionItem>
			<span slot="header">Archived To Dos</span>
			<TodoArchivedTable />
		</AccordionItem>
	</Accordion>
</div>
