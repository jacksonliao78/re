import { useState } from "react";
import JobCard from "./JobCard";
import type { Job } from '../types'
import { fetchJobs } from '../api/jobs';

type SelectorPayload = { type: string; intern: boolean; fullTime: boolean };

type Props = {
  query?: SelectorPayload;
}

export default function JobList( { query }: Props ) {
    const [jobs, setJobs] = useState< Job[] >([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function onScrape() {
        console.log(`onScrape called at ${new Date().toISOString()}`, { query });
        setLoading(true);
        setError(null);
        try {
            const res = await fetchJobs(query);
            console.log(`fetchJobs returned ${res?.length ?? 0} jobs`);
            setJobs(res || []);
        } catch (e: any) {
            setError(e?.message || 'Failed to fetch jobs');
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="job-list">
            <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
                <button onClick={onScrape} disabled={loading}>{loading ? 'Searching…' : 'Scrape jobs'}</button>
                {error && <div className="error">{error}</div>}
            </div>

            <div>
                {jobs.length === 0 && <div>No jobs yet.</div>}
                {jobs.map((j) => (
                    <JobCard key={j.id || j.title} job={j} onSelect={(id) => console.log('selected', id)} />
                ))}
            </div>
        </div>
    )
}