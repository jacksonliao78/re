import type { Job } from "../types"

type SelectorPayload = { type: string; intern: boolean; fullTime: boolean };

export async function fetchJobs(query?: SelectorPayload): Promise<Job[]> {
  console.log(`fetchJobs called at ${new Date().toISOString()}`, { query });
  if (query) {
    // convert selector payload to server SearchQuery shape
    const levels: string[] = [];
    if (query.intern) levels.push("internship");
    if (query.fullTime) levels.push("fulltime");

    const body = { type: query.type, level: levels };

    console.log(`fetchJobs posting to /jobs/search`, { body });

    const resp = await fetch("/jobs/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`fetchJobs failed: ${resp.status} ${text}`);
    }

    const a = resp.json()

    console.log(a)

    return a;
  }

  return []
}

export default { fetchJobs };
