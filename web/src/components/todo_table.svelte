<script lang="ts">
	import { Badge, Button, ButtonGroup, Checkbox, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
	import { ArchiveSolid, CircleMinusSolid, EditSolid } from "flowbite-svelte-icons";
	import { initialTodo } from "../constants";
	import { deleteToDo, updateToDo, updateToDoIsDone } from "../data/todo_crud";
	import { adjustTagColorStyle } from "../functions";
	import { currentTodos, todos } from "../store";
	import { PriorityColor } from "../types";
	import TodoForm from "./todo_form.svelte";

    let editingId: string | undefined = undefined;

    function startEdit(id: string) {
        editingId = id;
    }

    function cancelEdit() {
        editingId = "";
    }

</script>

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
        {#each $currentTodos as todo}
            {#if editingId === todo.id}
                <TodoForm 
                todo={todo} 
                onCancel={cancelEdit}
                submitLabel="Update"/>
            {:else}
            <TableBodyRow>
                <TableBodyCell class="!p-4">
                    <Checkbox checked={todo.isDone} on:click={
                        async () => {$todos = await updateToDoIsDone({...todo, isDone: !todo.isDone}, $todos)}} />
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
                        <Button on:click={() => startEdit(todo.id ?? "")}>
                            <EditSolid class="me-2 h-4 w-4" />
                            Edit
                        </Button>
                        <Button on:click={async () => {$todos = await updateToDo({...todo, isArchived: true}, $todos)}}>
                            <ArchiveSolid class="me-2 h-4 w-4" />
                            Archive
                        </Button>
                        <Button on:click={async () => {$todos = await deleteToDo(todo.id, $todos)}}>
                            <CircleMinusSolid class="me-2 h-4 w-4" />
                            Delete
                        </Button>
                    </ButtonGroup>
                </TableBodyCell>
            </TableBodyRow>
            {/if}
        {/each}
        <TodoForm 
        todo={initialTodo}
        submitLabel="Add"/>
    </TableBody>
</Table>
