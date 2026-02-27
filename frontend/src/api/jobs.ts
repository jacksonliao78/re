import type { Job } from "../types";

type SelectorPayload = { type: string; intern: boolean; fullTime: boolean };

export async function fetchJobs(query?: SelectorPayload, token?: string | null): Promise<Job[]> {
  if (!query) return [];
  const levels: string[] = [];
  if (query.intern) levels.push("internship");
  if (query.fullTime) levels.push("fulltime");
  const body = { type: query.type, level: levels };
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const resp = await fetch("/jobs/search", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`fetchJobs failed: ${resp.status} ${text}`);
  }
  return resp.json();
}

export default { fetchJobs };
