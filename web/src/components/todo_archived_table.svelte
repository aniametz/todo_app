<script lang="ts">
	import { Button, ButtonGroup, Checkbox, Table, TableBody, TableBodyCell, TableBodyRow } from "flowbite-svelte";
	import { ArrowUpRightFromSquareSolid, CircleMinusSolid } from "flowbite-svelte-icons";
	import { createEventDispatcher } from "svelte";
	import { archivedTodos } from "../store";

    const dispatch = createEventDispatcher();

    </script>

<div>

<Table hoverable={true}>
    <TableBody tableBodyClass="divide-y">
        {#each $archivedTodos as todo}
            <TableBodyRow>
                <TableBodyCell class="!p-4"
                    ><Checkbox checked={todo.isDone} disabled />
                </TableBodyCell>
                <TableBodyCell>{todo.description}</TableBodyCell>
                <TableBodyCell></TableBodyCell>
                <TableBodyCell>
                    <ButtonGroup class="*:!ring-primary-700">
                        <Button on:click={() => {dispatch("todoRestored", {...todo, isArchived: false})}}>
                            <ArrowUpRightFromSquareSolid class="me-2 h-4 w-4" />
                            Restore
                        </Button>
                        <Button on:click={() => dispatch("todoDeleted", todo.id)}>
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