export interface ToDo {
	id?: string;
	description: string;
	priority: Priority;
	difficulty?: number;
	tags: Tag[];
	isDone: boolean;
	isArchived: boolean;
	createdAt?: string;
	completedAt?: string;
	dueDate?: Date | undefined;
}

export enum Priority {
	NONE = 'none',
	LOW = 'low',
	MEDIUM = 'medium',
	HIGH = 'high'
}

export type FlowbiteBadgeColor =
	| 'red'
	| 'yellow'
	| 'green'
	| 'indigo'
	| 'purple'
	| 'pink'
	| 'blue'
	| 'primary'
	| 'secondary'
	| 'gray'
	| 'orange'
	| 'amber'
	| 'lime'
	| 'emerald'
	| 'teal'
	| 'cyan'
	| 'sky'
	| 'violet'
	| 'fuchsia'
	| 'rose'
	| undefined;

export const PriorityColor: Record<string, FlowbiteBadgeColor> = {
	[Priority.NONE]: undefined,
	[Priority.LOW]: 'green',
	[Priority.MEDIUM]: 'yellow',
	[Priority.HIGH]: 'red'
};

export interface Tag {
	id?: string;
	name: string;
	color?: string;
}
