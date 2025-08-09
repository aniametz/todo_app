export interface ToDo {
	id?: string;
	description: string;
	priority: Priority;
	isDone: boolean;
	isArchived: boolean;
	createdAt?: string;
	completedAt?: string;
}

export enum Priority {
	NONE = 'none',
	LOW = 'low',
	MEDIUM = 'medium',
	HIGH = 'high'
}

export type FlowbiteBadgeColor =
	| 'none'
	| 'red'
	| 'yellow'
	| 'green'
	| 'indigo'
	| 'purple'
	| 'pink'
	| 'blue'
	| 'dark'
	| 'primary'
	| undefined;

export const PriorityColor: Record<string, FlowbiteBadgeColor> = {
	[Priority.NONE]: 'none',
	[Priority.LOW]: 'green',
	[Priority.MEDIUM]: 'yellow',
	[Priority.HIGH]: 'red'
};
