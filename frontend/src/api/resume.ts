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
	} catch (e) {
		// ignore parse errors
	}

	return { ok: resp.ok, status: resp.status, data };
}

export default { uploadResume };
