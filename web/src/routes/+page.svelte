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
		MultiSelect,
		Select,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Tooltip
	} from 'flowbite-svelte';
	import {
		ArchiveSolid,
		ArrowUpRightFromSquareSolid,
		CircleMinusSolid,
		CirclePlusSolid,
		EditSolid
	} from 'flowbite-svelte-icons';
	import Navbar from './navbar.svelte';

	import Color from 'color';
	import { onMount } from 'svelte';
	import { createTagRequest, deleteTagRequest, getTagsRequest, validateTagRequest } from '../functions/tag_crud';
	import { createToDoRequest, deleteToDoRequest, getToDosRequest, updateToDoRequest } from '../functions/todo_crud';
	import { Priority, PriorityColor, type Tag, type ToDo } from "../types";

	let todos: ToDo[] = [];
	let tags: Tag[] = [];
	let tagItems: { value: string; name: string }[] = []

	onMount(async () => {
		todos = await getToDosRequest();
		tags = await getTagsRequest();
		tagItems = tags.map(tag => ({ value: tag.name, name: tag.name }));
	})

	let todoDescription: string = '';
	let todoPriority: Priority = Priority.NONE;
	let todoDifficulty: number | undefined = undefined;
	let todoDueDate: Date | undefined  = undefined;
	let todoDueDateTime: string | undefined  = undefined;
	let todoTags: string[] = [];
	let openAlert = false;

	async function resetToDoForm() {
		todoDescription = '';
		todoPriority = Priority.NONE;
		todoDifficulty = undefined;
		todoDueDate = undefined;
		todoDueDateTime = undefined;
		todoTags = [];
		todos = await getToDosRequest()
	}

	async function createToDo() {
		if (!todoDescription) {
			openAlert = true;
			setTimeout(() => {
				openAlert = false;
			}, 5000);
			return;
		}

		if (todoDueDateTime && todoDueDate) {
			todoDueDate = new Date(todoDueDate + ' ' + todoDueDateTime);
		}

		const newTodo = {
			description: todoDescription,
			priority: todoPriority,
			difficulty: todoDifficulty,
			dueDate: todoDueDate,
			tags: todoTags.map(tag => ({ name: tag})), 
			isDone: false,
			isArchived: false
		};
		console.log('Creating new todo:', newTodo);
		await createToDoRequest(newTodo);
		await resetToDoForm();
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

	const defaultTagColor = '#000000';
	let newTag: Tag = { name: '', color: defaultTagColor };;
	let openTagAlert = false;
	let alertMessage: string | undefined;

	async function createTag() {
		if (!newTag.name) {
			alertMessage = 'Tag name is required';
			openTagAlert = true;
			setTimeout(() => {
				alertMessage = undefined;
				openTagAlert = false;
			}, 5000);
			return;
		}
		const validationMessage = await validateTagRequest(newTag);
		if (validationMessage && validationMessage !== 'success') {
			alertMessage = validationMessage;
			openTagAlert = true;
			setTimeout(() => {
				alertMessage = undefined;
				openTagAlert = false;
			}, 5000);
			return
		}
		await createTagRequest(newTag);
		newTag = { name: '', color: defaultTagColor };
		tags = await getTagsRequest();
		tagItems = tags.map(tag => ({ value: tag.name, name: tag.name }));
	}

	async function updateTag(tag: Tag) {
		return
	}

	async function deleteTag(id: string | undefined) {
		if (!id) {
			return;
		}
		await deleteTagRequest(id);
		tags = await getTagsRequest();
		tagItems = tags.map(tag => ({ value: tag.name, name: tag.name }));
		todos = await getToDosRequest();
	}

	function adjustTagColorStyle(colorHex: string | undefined): string {
		const color = Color(colorHex || defaultTagColor);

		const accent = color.saturate(0.1).lightness(45)
		const backgorund = color.saturate(-0.2).lightness(90)

		return `border: 2px solid ${accent.hex()}; background-color: ${backgorund.hex()}; color: ${accent.hex()};`;
	}

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
					<TableHeadCell class="w-40">Difficulty</TableHeadCell>
					<TableHeadCell class="w-60">Due date</TableHeadCell>
					<TableHeadCell class="w-80">Tags</TableHeadCell>
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
								<Badge color={PriorityColor[todo.priority]}>
									{todo.priority.toUpperCase()}
								</Badge>
							</TableBodyCell>
							<TableBodyCell>{todo.difficulty ?? '---'}</TableBodyCell>
							<TableBodyCell>{todo.dueDate ?? '---'}</TableBodyCell>
							<TableBodyCell>
								{#if todo.tags && todo.tags.length > 0}
									{#each todo.tags as tag}
										<Badge style={adjustTagColorStyle(tag.color)} class="mr-1">{tag.name}</Badge>
									{/each}
								{:else}
									---
								{/if}
							</TableBodyCell>
							<TableBodyCell>
								<ButtonGroup class="*:!ring-primary-700">
									<Button>
										<EditSolid class="me-2 h-4 w-4" />
										Edit
									</Button>
									<Button on:click={() => updateToDo({...todo, isArchived: true})}>
										<ArchiveSolid class="me-2 h-4 w-4" />
										Archive
									</Button>
									<Button on:click={() => deleteToDo(todo.id)}>
										<CircleMinusSolid class="me-2 h-4 w-4" />
										Delete
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
								placeholder="Type todo description"
								size="sm"
								color={openAlert ? 'red' : undefined}
								bind:value={todoDescription}
							/>
						</TableBodyCell>
						<TableBodyCell class="w-40">
							<Select 
								id="todo-priority"
								placeholder="Select priority"
								bind:value={todoPriority} 
								size="sm">
								{#each Object.values(Priority) as priorityValue}
									<option value={priorityValue}>{priorityValue.toUpperCase()}</option>
								{/each}
							</Select>
							<Tooltip>Select priority</Tooltip>
						</TableBodyCell>
						<TableBodyCell class="w-40">
							<Input
								type="number"
								id="todo-difficulty"
								size="sm"
								min="1"
								max="5"
								bind:value={todoDifficulty}/>
							<Tooltip>Select difficulty (1-5)</Tooltip>
						</TableBodyCell>
						<TableBodyCell class="w-60">
							<Input
								type="date"
								id="todo-due-date"
								size="sm"
								bind:value={todoDueDate}/>
							<Tooltip>Select due date</Tooltip>
							<Input
								type="time"
								id="todo-due-time"
								size="sm"
								bind:value={todoDueDateTime}/>
						</TableBodyCell>
						<TableBodyCell class="w-80">
							<!-- TODO: fix the issue with Multiselect hidden dropdown -->
							<MultiSelect placeholder="Select tags" items={tagItems} bind:value={todoTags} />
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
			<span slot="header">Manage Tags</span>
			<Table hoverable={true}>
				<TableHead>
					<TableHeadCell>Name</TableHeadCell>
					<TableHeadCell class="w-60">Appearance</TableHeadCell>
					<TableHeadCell>Actions</TableHeadCell>
				</TableHead>
				<TableBody tableBodyClass="divide-y">
					{#each tags as tag}
						<TableBodyRow>
							<TableBodyCell>{tag.name}</TableBodyCell>
							<TableHeadCell>
								<Badge style={adjustTagColorStyle(tag.color)}>{tag.name}</Badge>
							</TableHeadCell>
							<TableBodyCell>
								<ButtonGroup class="*:!ring-primary-700">
									<Button on:click={() => updateTag(tag)}>
										<EditSolid class="me-2 h-4 w-4" />
										Edit
									</Button>
									<Button on:click={() => deleteTag(tag.id)}>
										<CircleMinusSolid class="me-2 h-4 w-4" />
										Delete
									</Button>
								</ButtonGroup>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
					<TableBodyRow>
						<TableBodyCell>
							<Input
								id="tag-name"
								size="sm"
								placeholder="Type tag name"
								color={openTagAlert ? 'red' : undefined}
								bind:value={newTag.name}
							/>
						</TableBodyCell>
						<TableBodyCell>
							<div class="flex items-center gap-2">
								<Input type="color" size="sm" bind:value={newTag.color} />
								<Tooltip>Select color</Tooltip>
								<Badge style={adjustTagColorStyle(newTag.color)}>new tag</Badge>
							</div>
						</TableBodyCell>
						<TableBodyCell>
							<ButtonGroup class="*:!ring-primary-700">
								<Button on:click={() => createTag()}>
									<CirclePlusSolid class="me-2 h-4 w-4" />
									Add
								</Button>
							</ButtonGroup>
						</TableBodyCell>
					</TableBodyRow>
				</TableBody>
			</Table>
			{#if openTagAlert}
				<Alert>{alertMessage}</Alert>
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
									<Button on:click={() => updateToDo({...todo, isArchived: false})}>
										<ArrowUpRightFromSquareSolid class="me-2 h-4 w-4" />
										Restore
									</Button>
									<Button on:click={() => deleteToDo(todo.id)}>
										<CircleMinusSolid class="me-2 h-4 w-4" />
										Delete
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
