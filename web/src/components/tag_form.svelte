<script lang="ts">
	import { Alert, Badge, Button, ButtonGroup, Input, TableBodyCell, TableBodyRow, Tooltip } from "flowbite-svelte";
	import { CirclePlusSolid, CloseCircleSolid, PenSolid } from "flowbite-svelte-icons";
	import { defaultTagColor } from "../constants";
	import { createTagRequest, updateTagRequest, validateTagRequest } from "../data/tag_crud";
	import { adjustTagColorStyle } from "../functions";
	import { loadTags, loadTodos, tags } from "../store";
	import type { Tag } from "../types";

    export let tag: Tag = { name: '', color: defaultTagColor };
    export let onCancel: () => void = () => {};
    export let submitLabel: string = "Add";

    let newTag = structuredClone(tag);

    const numberOfColumns = Object.keys(tag).length + 1;
	let openAlert = false;
	let alertMessage: string | undefined;

    function resetTagForm() {
        newTag = { name: '', color: defaultTagColor };
    }   

    async function validateTag(): Promise<boolean> {
        if (!newTag.name) alertMessage = 'Name is required';
		const validationMessage = await validateTagRequest(newTag);
		if (validationMessage && validationMessage !== 'success') alertMessage = validationMessage;

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

	async function createTag() {
        const isTagValid = await validateTag();
		if (isTagValid) {
            await createTagRequest(newTag);
            // adding new tag to the store results in missing tag id from database
            await loadTags();
		    resetTagForm();
        }
	}

    async function updateTag() {
        const isTagValid = await validateTag();
        if (isTagValid) {
            await updateTagRequest(newTag);
            $tags = $tags.map(item => {
                if (item.id === newTag.id) return newTag;
                return item;
            });
            await loadTodos();
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
            color={openAlert ? 'red' : undefined}
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
                <Button onclick={() => createTag()}>
                    <CirclePlusSolid class="me-2 h-4 w-4" />
                    Add
                </Button>
            {:else}
                <Button onclick={() => updateTag()}>
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