<script lang="ts">
	import { Badge, Button, ButtonGroup, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
	import { CircleMinusSolid, EditSolid } from "flowbite-svelte-icons";
	import { createEventDispatcher, onMount } from "svelte";
	import { defaultTagColor } from "../constants";
	import { deleteTagRequest, getTagsRequest } from "../data/tag_crud";
	import { adjustTagColorStyle } from "../functions";
	import type { Tag } from "../types";
	import TagForm from "./tag_form.svelte";

    const dispatch = createEventDispatcher();

    let tags: Tag[] = [];

    async function handleTagsUpdate() {
        tags = await getTagsRequest();
        dispatch('tagsUpdated', tags);
    }

    onMount(async () => await handleTagsUpdate())

    async function deleteTag(id: string | undefined) {
		if (!id) {
			return;
		}
		await deleteTagRequest(id);
        await handleTagsUpdate()
        dispatch('tagDeleted');
	}

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
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell class="w-60">Appearance</TableHeadCell>
        <TableHeadCell>Actions</TableHeadCell>
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        {#each tags as tag}
            {#if editingId === tag.id}
                <TagForm 
                tag={tag} 
                on:tagsNeedUpdate={async () => await handleTagsUpdate()} 
                onCancel={cancelEdit}
                submitLabel="Update"/>
            {:else}
            <TableBodyRow>
                <TableBodyCell>{tag.name}</TableBodyCell>
                <TableHeadCell>
                    <Badge style={adjustTagColorStyle(tag.color)}>{tag.name}</Badge>
                </TableHeadCell>
                <TableBodyCell>
                    <ButtonGroup class="*:!ring-primary-700">
                        <Button on:click={() => startEdit(tag.id ?? "")}>
                            <EditSolid  class="me-2 h-4 w-4" />
                            Edit
                        </Button>
                        <Button on:click={() => deleteTag(tag.id)}>
                            <CircleMinusSolid class="me-2 h-4 w-4" />
                            Delete
                        </Button>
                    </ButtonGroup>
                </TableBodyCell>
            </TableBodyRow>
            {/if}
        {/each}
        <TagForm 
        tag={{ name: '', color: defaultTagColor }}
        on:tagsNeedUpdate={async () => await handleTagsUpdate()} 
        submitLabel="Add"/>
    </TableBody>
</Table>
