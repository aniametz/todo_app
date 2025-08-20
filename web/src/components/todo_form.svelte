<script lang="ts">
	import { Alert, Button, ButtonGroup, Checkbox, Input, MultiSelect, Select, TableBodyCell, TableBodyRow, Tooltip } from "flowbite-svelte";
	import { CirclePlusSolid, CloseCircleSolid, PenSolid } from "flowbite-svelte-icons";
	import { initialTodo } from "../constants";
	import { createToDoRequest, updateToDo, validateTodoRequest } from "../data/todo_crud";
	import { loadTodos, tagItems, tags, todos } from "../store";
	import { Priority, type ToDo } from "../types";

    export let todo: ToDo = initialTodo;

    export let onCancel: () => void = () => {};
    export let submitLabel: string = "Add";

    let newTodo = structuredClone(todo);
    // TODO clean up date time conversion mess on web also
    const date = newTodo.dueDate ? new Date(newTodo.dueDate) : new Date();
    let todoDueDateEdit: string | undefined = 
    `${date.getUTCFullYear()}-${(date.getUTCMonth() + 1).toString().padStart(2, '0')}-${date.getUTCDate().toString().padStart(2, '0')}`;
	let todoDueDateTimeEdit: string | undefined  = 
    `${date.getUTCHours().toString().padStart(2, '0')}:${date.getUTCMinutes().toString().padStart(2, '0')}`;
    let todoTags: string[] = todo.tags ? todo.tags.map(tag => tag.name) : [];

    let todoDueDate: string | undefined = submitLabel === "Add" ? undefined : todoDueDateEdit;
    let todoDueDateTime: string | undefined = submitLabel === "Add" ? undefined : todoDueDateTimeEdit;

    const numberOfColumns = Object.keys(todo).length + 1;
    let alertMessage: string | undefined  = undefined;
	let openAlert = false;

	async function resetToDoForm() {
        newTodo = initialTodo;
        todoDueDateEdit = undefined;
        todoDueDateTimeEdit = undefined;
        todoDueDate = undefined;
		todoDueDateTime = undefined;
        todoTags = [];
	}

    async function validateTodo(): Promise<boolean> {
        if (!newTodo.description) alertMessage = 'Description is required';
		const validationMessage = await validateTodoRequest(newTodo);
		if (validationMessage && validationMessage !== 'success') alertMessage = validationMessage;
        if (!todoDueDate && todoDueDateTime) alertMessage = 'Due date is required when time is set';

        if (alertMessage) {
            openAlert = true;
			setTimeout(() => {
				alertMessage = undefined;
				openAlert = false;
			}, 5000);
			return false;
        }
        return true;
    }

	async function createToDo() {
        const isTodoValid = await validateTodo();
		if (isTodoValid) {
            todoDueDateTime = todoDueDateTime ? todoDueDateTime : "00:00";
            if (todoDueDateTime) newTodo.dueDate = new Date(todoDueDate + ' ' + todoDueDateTime);
            newTodo.tags = $tags.filter(tag => todoTags.includes(tag.name))
            await createToDoRequest(newTodo);
            // adding new todo to the store results in missing todo id from database
            await loadTodos();
            resetToDoForm();
        }
	}

</script>

<TableBodyRow>
    <TableBodyCell class="!p-4">
        <Checkbox disabled />
    </TableBodyCell>
    <TableBodyCell>
        <Input
            id="todo-description"
            placeholder="Type todo description"
            size="sm"
            color={openAlert && alertMessage?.includes("Description") ? 'red' : undefined}
            bind:value={newTodo.description}
        />
    </TableBodyCell>
    <TableBodyCell class="w-40">
        <Select 
            id="todo-priority"
            placeholder="Select priority"
            bind:value={newTodo.priority} 
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
            bind:value={newTodo.difficulty}/>
        <Tooltip>Select difficulty (1-5)</Tooltip>
    </TableBodyCell>
    <TableBodyCell class="w-60">
        <Input
            type="date"
            id="todo-due-date"
            size="sm"
            color={openAlert && alertMessage?.includes("Due date") ? 'red' : undefined}
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
        <MultiSelect placeholder="Select tags" items={$tagItems} bind:value={todoTags} />
    </TableBodyCell>
    <TableBodyCell>
        <ButtonGroup class="*:!ring-primary-700">
        </ButtonGroup>
                <ButtonGroup class="*:!ring-primary-700">
            {#if submitLabel === "Add"}
                <Button on:click={() => createToDo()}>
                    <CirclePlusSolid class="me-2 h-4 w-4" />
                    Add
                </Button>
            {:else}
                <Button on:click={async () => {$todos = await updateToDo({
                    ...newTodo, 
                    tags: $tags.filter(tag => todoTags.includes(tag.name)), 
                    dueDate:  (todoDueDateTime && todoDueDate) ? new Date(todoDueDate + ' ' + todoDueDateTime) : undefined,
                    }, $todos);
                    onCancel();}}>
                    <PenSolid class="me-2 h-4 w-4" />
                    Update
                </Button>
                <Button on:click={() => onCancel()}>
                    <CloseCircleSolid class="me-2 h-4 w-4" />
                    Cancel
                </Button>
            {/if}
        </ButtonGroup>
    </TableBodyCell>
</TableBodyRow>
{#if openAlert}
<TableBodyRow>
    <TableBodyCell colspan={numberOfColumns}>
        <Alert>{alertMessage}</Alert>
    </TableBodyCell>
</TableBodyRow>
{/if}
