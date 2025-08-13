import axios from 'axios';
import { backend_port } from '../constants';
import type { ToDo } from '../types';

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
