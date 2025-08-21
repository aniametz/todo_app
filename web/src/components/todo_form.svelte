<script lang="ts">
	import { Alert, Button, ButtonGroup, Checkbox, Datepicker, Input, MultiSelect, Select, TableBodyCell, TableBodyRow } from "flowbite-svelte";
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
    let todoDueDateEdit: string | undefined = date.getDate() + '-' + (date.getMonth() + 1) + '-' + date.getFullYear();
	let todoDueDateTimeEdit: string | undefined  = date.toTimeString().slice(0, 5);
    let todoTags: string[] = todo.tags ? todo.tags.map(tag => tag.name) : [];

    let todoDueDate: Date | undefined = undefined;
    let todoDueDateTime: string | undefined = undefined;

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
        if (newTodo.difficulty && (newTodo.difficulty < 1 || newTodo.difficulty > 5 )) alertMessage = 'Difficulty must be between 1 and 5';

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

    function joinDueDateWithTime() {
        if (todoDueDateTime && todoDueDate) {
            const time = todoDueDateTime.split(':').map(Number);
            todoDueDate.setHours(todoDueDate.getHours() + time[0]);
            todoDueDate.setMinutes(todoDueDate.getMinutes() + time[1]);
            return todoDueDate;
        }
        else {
            return todoDueDate;
        }
    }

	async function createToDo() {
        const isTodoValid = await validateTodo();
		if (isTodoValid) { 
            newTodo.dueDate = joinDueDateWithTime();
            newTodo.tags = $tags.filter(tag => todoTags.includes(tag.name))
            await createToDoRequest(newTodo);
            // adding new todo to the store results in missing todo id from database
            await loadTodos();
            resetToDoForm();
        }
	}

</script>

<TableBodyRow>
    <TableBodyCell class="w-5">
        <Checkbox disabled />
    </TableBodyCell>
    <TableBodyCell>
        <Input
            id="todo-description"
            size="sm"
            color={openAlert && alertMessage?.includes("Description") ? 'red' : undefined}
            bind:value={newTodo.description}
        />
    </TableBodyCell>
    <TableBodyCell class="w-20">
        <Select 
            id="todo-priority"
            bind:value={newTodo.priority} 
            size="sm">
            {#each Object.values(Priority) as priorityValue}
                <option value={priorityValue}>{priorityValue.toUpperCase()}</option>
            {/each}
        </Select>
    </TableBodyCell>
    <TableBodyCell class="w-20">
        <Input
            type="number"
            id="todo-difficulty"
            size="sm"
            min="1"
            max="5"
            color={openAlert && alertMessage?.includes("Difficulty") ? 'red' : undefined}
            bind:value={newTodo.difficulty}/>
    </TableBodyCell>
    <TableBodyCell class="w-60">
        <div class="flex items-center gap-2">
        <Datepicker
            id="todo-due-datepicker"
            bind:value={todoDueDate}
            color={openAlert && alertMessage?.includes("Due date") ? 'red' : undefined} 
            />
        <Input
            type="time"
            id="todo-due-time"
            size="sm"
            class="w-20"
            bind:value={todoDueDateTime}/>
        </div>
    </TableBodyCell>
    <TableBodyCell class="w-80">
        <MultiSelect items={$tagItems} bind:value={todoTags} />
    </TableBodyCell>
    <TableBodyCell>
        <ButtonGroup class="*:!ring-primary-700">
            {#if submitLabel === "Add"}
                <Button onclick={() => createToDo()}>
                    <CirclePlusSolid class="me-2 h-4 w-4" />
                    Add
                </Button>
            {:else}
                <Button onclick={async () => {$todos = await updateToDo({
                    ...newTodo, 
                    tags: $tags.filter(tag => todoTags.includes(tag.name)), 
                    dueDate:  joinDueDateWithTime(),
                    }, $todos);
                    onCancel();}}>
                    <PenSolid class="me-2 h-4 w-4" />
                    Update
                </Button>
                <Button onclick={() => onCancel()}>
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
