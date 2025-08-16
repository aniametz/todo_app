import { Priority, type Tag, type ToDo } from './types';

export const backend_port = 'http://127.0.0.1:5000';

export const initialTodo: ToDo = {
	description: '',
	priority: Priority.NONE,
	difficulty: undefined,
	dueDate: undefined,
	tags: [],
	isDone: false,
	isArchived: false
};

export const defaultTagColor = '#000000';
export const initialTag: Tag = { name: '', color: defaultTagColor };
