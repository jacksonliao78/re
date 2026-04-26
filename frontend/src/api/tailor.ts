import type { Suggestion, Resume, Job } from "../types";

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

export async function getSuggestions(resume: Resume, job: Job, token?: string | null): Promise<Suggestion[]> {
    try {
        const headers: Record<string, string> = { "Content-Type": "application/json" };
        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }
        const resp = await fetch("/resume/tailor", {
            method: "POST",
            headers,
            body: JSON.stringify({ resume, job }),
        });

        if (!resp.ok) {
            const detail = await getErrorDetail(resp);
            throw new Error(`Failed to get suggestions: ${resp.status} ${detail}`);
        }

        const suggestions = await resp.json() as Suggestion[];
        return suggestions;
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        throw error;
    }
}