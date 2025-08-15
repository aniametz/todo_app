<script lang="ts">
	import { Alert, Badge, Button, ButtonGroup, Input, TableBodyCell, TableBodyRow, Tooltip } from "flowbite-svelte";
	import { CirclePlusSolid, CloseCircleSolid, PenSolid } from "flowbite-svelte-icons";
	import { createEventDispatcher } from "svelte";
	import { defaultTagColor } from "../constants";
	import { createTagRequest, updateTagRequest, validateTagRequest } from "../data/tag_crud";
	import { adjustTagColorStyle } from "../functions";
	import type { Tag } from "../types";

    const dispatch = createEventDispatcher();

    export let tag: Tag = { name: '', color: defaultTagColor };
    export let onCancel: () => void = () => {};
    export let submitLabel: string = "Add";

    let newTag = structuredClone(tag);
	let openTagAlert = false;
	let alertMessage: string | undefined;

    function resetTagForm() {
        newTag = { name: '', color: defaultTagColor }; 
        dispatch('tagsNeedUpdate');
    }   

    async function validateTag(tag: Tag): Promise<boolean> {
        if (!tag.name) {
			alertMessage = 'Tag name is required';
			openTagAlert = true;
			setTimeout(() => {
				alertMessage = undefined;
				openTagAlert = false;
			}, 5000);
			return false;
		}
		const validationMessage = await validateTagRequest(tag);
		if (validationMessage && validationMessage !== 'success') {
			alertMessage = validationMessage;
			openTagAlert = true;
			setTimeout(() => {
				alertMessage = undefined;
				openTagAlert = false;
			}, 5000);
			return false;
		}
        return true;
    }

	async function createTag() {
        const isTagValid = await validateTag(newTag);
		if (isTagValid) {
            await createTagRequest(newTag);
		    resetTagForm()
        }
	}

    async function updateTag() {
        const isTagValid = await validateTag(newTag);
        if (isTagValid) {
            await updateTagRequest(newTag);
            resetTagForm();
            onCancel();
        }
	}

</script>

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
            {#if submitLabel === "Add"}
                <Button on:click={() => createTag()}>
                    <CirclePlusSolid class="me-2 h-4 w-4" />
                    Add
                </Button>
            {:else}
                <Button on:click={() => updateTag()}>
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
{#if openTagAlert}
    <Alert>{alertMessage}</Alert>
{/if}