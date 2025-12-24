import type { Suggestion, Resume, Job } from "../types";

export async function getSuggestions(resume: Resume, job: Job): Promise<Suggestion[]> {
    try {
        const resp = await fetch("/resume/tailor", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resume, job }),
        });

        if (!resp.ok) {
            const text = await resp.text();
            throw new Error(`Failed to get suggestions: ${resp.status} ${text}`);
        }

        const suggestions = await resp.json() as Suggestion[];
        return suggestions;
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        throw error;
    }
}