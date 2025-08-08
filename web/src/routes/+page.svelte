<script lang='ts'>

	import {
		Accordion,
		AccordionItem,
		Alert,
		Badge,
		Button,
		ButtonGroup,
		Checkbox,
		Input,
		Select,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import {
		ArchiveSolid,
		ArrowUpRightFromSquareSolid,
		CircleMinusSolid,
		CirclePlusSolid
	} from 'flowbite-svelte-icons';
	import Navbar from './navbar.svelte';

	import { onMount } from 'svelte';
	import { createToDoRequest, deleteToDoRequest, getToDosRequest, updateToDoRequest } from '../functions/todo_crud';
	import { Priority, PriorityColor, type ToDo } from "../types";

	let todos: ToDo[] = [];

	onMount(async () => (todos = await getToDosRequest()))

	let todoDescription: string = '';
	let todoPriority: Priority | null = null;
	let openAlert = false;

	async function createToDo() {
		if (!todoDescription) {
			openAlert = true;
			setTimeout(() => {
				openAlert = false;
			}, 5000);
			return;
		}
		const newTodo = {
			description: todoDescription,
			priority: todoPriority,
			isDone: false,
			isArchived: false
		};
		await createToDoRequest(newTodo);
		todoDescription = '';
		todoPriority = null;
		todos = await getToDosRequest()
	}

	async function updateToDo(todo: ToDo) {
		await updateToDoRequest(todo);
		todos = await getToDosRequest()
	}

	async function deleteToDo(id: string | undefined) {
		if (!id) {
			return;
		}
		await deleteToDoRequest(id);
		todos = await getToDosRequest()
	}

	$: currentTodos = todos.filter((item) => !item.isArchived);
	$: archivedTodos = todos.filter((item) => item.isArchived);
</script>

<Navbar></Navbar>

<div class="text-center">
	<Accordion>
		<AccordionItem open>
			<span slot="header">Current To Dos</span>
			<Table hoverable={true}>
				<TableHead>
					<TableHeadCell class="!p-4"></TableHeadCell>
					<TableHeadCell>Description</TableHeadCell>
					<TableHeadCell class="w-40">Priority</TableHeadCell>
					<TableHeadCell>Actions</TableHeadCell>
				</TableHead>
				<TableBody tableBodyClass="divide-y">
					{#each currentTodos as todo}
						<TableBodyRow>
							<TableBodyCell class="!p-4">
								<Checkbox checked={todo.isDone} on:click={() => updateToDo({...todo, isDone: !todo.isDone})} />
							</TableBodyCell>
							<TableBodyCell>{todo.description}</TableBodyCell>
							<TableBodyCell class="w-40">
								<Badge color={PriorityColor[todo.priority ?? 'none']}>
									{todo.priority ? todo.priority.toUpperCase() : 'NONE'}
								</Badge>
							</TableBodyCell>
							<TableBodyCell>
								<ButtonGroup class="*:!ring-primary-700">
									<Button on:click={() => deleteToDo(todo.id)}>
										<CircleMinusSolid class="me-2 h-4 w-4" />
										Delete
									</Button>
									<Button on:click={() => updateToDo({...todo, isArchived: true})}>
										<ArchiveSolid class="me-2 h-4 w-4" />
										Archive
									</Button>
								</ButtonGroup>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
					<TableBodyRow>
						<TableBodyCell class="!p-4">
							<Checkbox disabled />
						</TableBodyCell>
						<TableBodyCell>
							<Input
								id="todo-description"
								size="sm"
								color={openAlert ? 'red' : undefined}
								bind:value={todoDescription}
							/>
						</TableBodyCell>
						<TableBodyCell class="w-40">
							<Select 
								id="todo-priority"
								placeholder="Select priority"
								bind:value={todoPriority} size="sm">
								<option value={null}>NONE</option>
								{#each Object.values(Priority) as value}
									<option value={value}>{value.toUpperCase()}</option>
								{/each}
							</Select>
						</TableBodyCell>
						<TableBodyCell>
							<ButtonGroup class="*:!ring-primary-700">
								<Button on:click={() => createToDo()}>
									<CirclePlusSolid class="me-2 h-4 w-4" />
									Add
								</Button>
							</ButtonGroup>
						</TableBodyCell>
					</TableBodyRow>
				</TableBody>
			</Table>
			{#if openAlert}
				<Alert>To Do description is required</Alert>
			{/if}
		</AccordionItem>

		<AccordionItem>
			<span slot="header">Archived To Dos</span>
			<Table hoverable={true}>
				<TableBody tableBodyClass="divide-y">
					{#each archivedTodos as todo}
						<TableBodyRow>
							<TableBodyCell class="!p-4"
								><Checkbox checked={todo.isDone} disabled />
							</TableBodyCell>
							<TableBodyCell>{todo.description}</TableBodyCell>
							<TableBodyCell></TableBodyCell>
							<TableBodyCell>
								<ButtonGroup class="*:!ring-primary-700">
									<Button on:click={() => deleteToDo(todo.id)}>
										<CircleMinusSolid class="me-2 h-4 w-4" />
										Delete
									</Button>
									<Button on:click={() => updateToDo({...todo, isArchived: false})}>
										<ArrowUpRightFromSquareSolid class="me-2 h-4 w-4" />
										Restore
									</Button>
								</ButtonGroup>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
				</TableBody>
			</Table>
		</AccordionItem>
	</Accordion>
</div>
