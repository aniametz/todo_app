import { derived, writable } from 'svelte/store';
import { getTagsRequest } from './data/tag_crud';
import { getToDosRequest } from './data/todo_crud';
import type { Tag, ToDo } from './types';

export const todos = writable<ToDo[]>([]);

export async function loadTodos() {
	const data = await getToDosRequest();
	todos.set(data);
}

export const currentTodos = derived(todos, ($todos) => $todos.filter((todo) => !todo.isArchived));
export const archivedTodos = derived(todos, ($todos) => $todos.filter((todo) => todo.isArchived));

export const tags = writable<Tag[]>([]);

export async function loadTags() {
	const data = await getTagsRequest();
	tags.set(data);
}

export const tagItems = derived(tags, ($tags) =>
	$tags.map((tag) => ({ value: tag.name, name: tag.name }))
);
