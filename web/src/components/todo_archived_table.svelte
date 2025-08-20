<script lang="ts">
	import { Button, ButtonGroup, Checkbox, Table, TableBody, TableBodyCell, TableBodyRow } from "flowbite-svelte";
	import { ArrowUpRightFromSquareSolid, CircleMinusSolid } from "flowbite-svelte-icons";
	import { deleteToDo, updateToDo } from "../data/todo_crud";
	import { archivedTodos, todos } from "../store";

</script>

<div>

<Table hoverable={true}>
    <TableBody class="divide-y">
        {#each $archivedTodos as todo}
            <TableBodyRow>
                <TableBodyCell class="!p-4"
                    ><Checkbox checked={todo.isDone} disabled />
                </TableBodyCell>
                <TableBodyCell>{todo.description}</TableBodyCell>
                <TableBodyCell></TableBodyCell>
                <TableBodyCell>
                    <ButtonGroup class="*:!ring-primary-700">
                        <Button onclick={async () => {$todos = await updateToDo({...todo, isArchived: false}, $todos)}}>
                            <ArrowUpRightFromSquareSolid class="me-2 h-4 w-4" />
                            Restore
                        </Button>
                        <Button onclick={async () => $todos = await deleteToDo(todo.id, $todos)}>
                            <CircleMinusSolid class="me-2 h-4 w-4" />
                            Delete
                        </Button>
                    </ButtonGroup>
                </TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>
</div>