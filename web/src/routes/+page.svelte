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
	import { deleteToDoRequest, updateToDoIsDoneRequest, updateToDoRequest } from '../data/todo_crud';
	import { loadTags, loadTodos, todos } from '../store';
	import { type ToDo } from "../types";

	onMount(async () => {await loadTodos(); await loadTags()});

	async function updateToDo(todo: ToDo) {
		await updateToDoRequest(todo);
		$todos = $todos.map(item => {
			if (item.id === todo.id) return todo;
			return item;
		});
	}

	async function updateToDoIsDone(todo: ToDo) {
		await updateToDoIsDoneRequest(todo);
		$todos = $todos.map(item => {
			if (item.id === todo.id) return todo;
			return item;
		});
	}

	async function deleteToDo(id: string | undefined) {
		if (!id) {
			return;
		}
		await deleteToDoRequest(id);
		$todos = $todos .filter(item => item.id !== id);
	}

</script>

<Navbar></Navbar>

<div class="text-center">
	<Accordion>
		<AccordionItem open>
			<span slot="header">Current To Dos</span>
			<TodoTable
				on:updateToDo={(event) => updateToDo(event.detail)}
				on:updateToDoIsDone={(event) => updateToDoIsDone(event.detail)}
				on:deleteToDo={(event) => deleteToDo(event.detail)}
				/>
		</AccordionItem>

		<AccordionItem>
			<span slot="header">Manage Tags</span>
			<TagsTable/>
		</AccordionItem>

		<AccordionItem>
			<span slot="header">Archived To Dos</span>
			<TodoArchivedTable
				on:todoRestored={(event) => updateToDo(event.detail)}
				on:todoDeleted={(event) => deleteToDo(event.detail)}
				/>
		</AccordionItem>
	</Accordion>
</div>
