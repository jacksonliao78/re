export async function uploadResume(file: File) {
	const form = new FormData();
	form.append("file", file);

	const resp = await fetch("/resume/upload", {
		method: "POST",
		body: form,
	});

	let data = null;
	try {
		data = await resp.json();
	} catch {
		// ignore parse errors
	}

	return { ok: resp.ok, status: resp.status, data };
}

async function getErrorDetail(resp: Response): Promise<string> {
	try {
		const data = await resp.json();
		if (data && typeof data.detail === "string" && data.detail.trim()) {
			return data.detail;
		}
		return JSON.stringify(data);
	} catch {
		return await resp.text();
	}
}

type CreateKnowledgeInput = {
	title: string;
	content: string;
	sourceType?: string;
};

export async function getKnowledgeDocuments(token: string) {
	const resp = await fetch("/resume/knowledge", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
	});
	if (!resp.ok) {
		const detail = await getErrorDetail(resp);
		throw new Error(`Failed to load knowledge documents: ${resp.status} ${detail}`);
	}
	return resp.json();
}

export async function createKnowledgeDocument(input: CreateKnowledgeInput, token: string) {
	const resp = await fetch("/resume/knowledge", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
		body: JSON.stringify(input),
	});
	if (!resp.ok) {
		const detail = await getErrorDetail(resp);
		throw new Error(`Failed to create knowledge document: ${resp.status} ${detail}`);
	}
	return resp.json();
}

export async function getKnowledgeDocumentById(id: string, token: string) {
	const resp = await fetch(`/resume/knowledge/${encodeURIComponent(id)}`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
	});
	if (!resp.ok) {
		const detail = await getErrorDetail(resp);
		throw new Error(`Failed to load context entry: ${resp.status} ${detail}`);
	}
	return resp.json();
}

export async function deleteKnowledgeDocument(id: string, token: string) {
	const resp = await fetch(`/resume/knowledge/${encodeURIComponent(id)}`, {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
	});
	if (!resp.ok) {
		const detail = await getErrorDetail(resp);
		throw new Error(`Failed to delete context entry: ${resp.status} ${detail}`);
	}
	if (resp.status === 204) return null;
	return resp.json();
}

export default {
	uploadResume,
	getKnowledgeDocuments,
	createKnowledgeDocument,
	getKnowledgeDocumentById,
	deleteKnowledgeDocument,
};
