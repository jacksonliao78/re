export async function updateQuery(query: { type: string; intern: boolean; fullTime: boolean }) {
  const resp = await fetch("/jobs/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(query),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`updateQuery failed: ${resp.status} ${text}`);
  }

  return resp.json().catch(() => null);
}

export default { updateQuery };
 
