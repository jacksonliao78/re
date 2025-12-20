import type { Job } from "../types"

type SelectorPayload = { type: string; intern: boolean; fullTime: boolean };

export async function fetchJobs(query?: SelectorPayload): Promise<Job[]> {
  if (query) {
    // convert selector payload to server SearchQuery shape
    const levels: string[] = [];
    if (query.intern) levels.push("intern");
    if (query.fullTime) levels.push("fulltime");

    const body = { type: query.type, level: levels };

    const resp = await fetch("/jobs/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`fetchJobs failed: ${resp.status} ${text}`);
    }

    return resp.json();
  }

  return []
}

export default { fetchJobs };
