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
			{#snippet header()}Current To Dos{/snippet}
			<TodoTable/>
		</AccordionItem>

		<AccordionItem>
			{#snippet header()}Manage Tags{/snippet}
			<TagsTable/>
		</AccordionItem>

		<AccordionItem>
			{#snippet header()}Archived To Dos{/snippet}
			<TodoArchivedTable />
		</AccordionItem>
	</Accordion>
</div>
