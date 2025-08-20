import axios from 'axios';
import { backend_port } from '../constants';
import type { ToDo } from '../types';

export async function validateTodoRequest(tagData: ToDo): Promise<string> {
	return await axios
		.post(backend_port + '/validate_todo', {
			todoData: tagData
		})
		.then((response) => response.data.message);
}

export async function createToDoRequest(todoData: ToDo): Promise<string> {
	return await axios
		.post(backend_port + '/create_todo', {
			todoData: todoData
		})
		.then((response) => response.data.message);
}

export async function updateToDoRequest(todoData: ToDo): Promise<string> {
	return await axios
		.post(backend_port + '/update_todo', {
			todoData: todoData
		})
		.then((response) => response.data.message);
}

export async function updateToDoIsDoneRequest(todoData: ToDo): Promise<string> {
	return await axios
		.post(backend_port + '/update_todo_is_done', {
			todoData: todoData
		})
		.then((response) => response.data.message);
}

export async function deleteToDoRequest(todoData: string): Promise<string> {
	return await axios
		.post(backend_port + '/delete_todo', {
			todoData: todoData
		})
		.then((response) => response.data.message);
}

export async function getToDosRequest(): Promise<ToDo[]> {
	return await axios.get(backend_port + '/get_todos').then((response) => response.data.todos);
}

export async function updateToDo(todo: ToDo, todoStore: ToDo[]): Promise<ToDo[]> {
	await updateToDoRequest(todo);
	return todoStore.map((item) => {
		if (item.id === todo.id) return todo;
		return item;
	});
}

export async function updateToDoIsDone(todo: ToDo, todoStore: ToDo[]): Promise<ToDo[]> {
	await updateToDoIsDoneRequest(todo);
	return todoStore.map((item) => {
		if (item.id === todo.id) return todo;
		return item;
	});
}

export async function deleteToDo(id: string | undefined, todoStore: ToDo[]): Promise<ToDo[]> {
	if (!id) {
		return todoStore;
	}
	await deleteToDoRequest(id);
	return todoStore.filter((item) => item.id !== id);
}
