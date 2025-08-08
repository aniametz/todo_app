export interface ToDo {
	id?: string;
	description: string;
	priority?: Priority | null;
	isDone: boolean;
	isArchived: boolean;
	createdAt?: string;
	completedAt?: string;
}

export enum Priority {
	Low = 'low',
	Medium = 'medium',
	High = 'high'
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

export const PriorityColor: Record<string | 'none', FlowbiteBadgeColor> = {
	none: 'none',
	[Priority.Low]: 'green',
	[Priority.Medium]: 'yellow',
	[Priority.High]: 'red'
};
