<script lang="ts">
	import { Alert, Badge, Button, ButtonGroup, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Tooltip } from "flowbite-svelte";
	import { CircleMinusSolid, CirclePlusSolid, EditSolid } from "flowbite-svelte-icons";
	import { createEventDispatcher, onMount } from "svelte";
	import { defaultTagColor } from "../constants";
	import { createTagRequest, deleteTagRequest, getTagsRequest, validateTagRequest } from "../data/tag_crud";
	import { adjustTagColorStyle } from "../functions";
	import type { Tag } from "../types";

    const dispatch = createEventDispatcher();

    let tags: Tag[] = [];

    onMount(async () => {
		tags = await getTagsRequest();
        dispatch('tagsUpdated', tags);
	})
    	
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
        dispatch('tagsUpdated', tags);
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
        dispatch('tagsUpdated', tags);
        dispatch('tagDeleted');
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
                    <Badge style={adjustTagColorStyle(newTag.color)}>{newTag.name != "" ? newTag.name : "new tag"}</Badge>
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