import axios from 'axios';
import { backend_port } from '../constants';
import type { Tag } from '../types';

export async function validateTagRequest(tagData: Tag): Promise<string> {
	return await axios
		.post(backend_port + '/validate_tag', {
			tagData: tagData
		})
		.then((response) => response.data.message);
}

export async function createTagRequest(tagData: Tag): Promise<string> {
	return await axios
		.post(backend_port + '/create_tag', {
			tagData: tagData
		})
		.then((response) => response.data.message);
}

export async function updateTagRequest(tagData: Tag): Promise<string> {
	return await axios
		.post(backend_port + '/update_tag', {
			tagData: tagData
		})
		.then((response) => response.data.message);
}

export async function deleteTagRequest(tagData: string): Promise<string> {
	return await axios
		.post(backend_port + '/delete_tag', {
			tagData: tagData
		})
		.then((response) => response.data.message);
}

export async function getTagsRequest(): Promise<Tag[]> {
	return await axios.get(backend_port + '/get_tags').then((response) => response.data.tags);
}
