import { useState } from "react";
import JobCard from "./JobCard";
import type { Job } from '../types'
import { fetchJobs } from '../api/jobs';

type SelectorPayload = { type: string; intern: boolean; fullTime: boolean };

type Props = {
  query?: SelectorPayload;
  onTailor?: (job: Job) => void;
  onIgnore?: (job: Job) => void;
  token?: string | null;
}

export default function JobList( { query, onTailor, onIgnore, token }: Props ) {
    const [jobs, setJobs] = useState< Job[] >([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function onScrape() {
        if (!query) return;
        setLoading(true);
        setError(null);
        try {
            const res = await fetchJobs(query, token);
            setJobs(res || []);
        } catch (e: any) {
            setError(e?.message || 'Failed to fetch jobs');
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="job-list">
            <div style={{ display: 'flex', gap: 8, marginBottom: 8, alignItems: 'center' }}>
                <button onClick={onScrape} disabled={loading}>{loading ? 'Searching…' : 'Scrape jobs'}</button>
                {error && <div className="error" style={{ color: 'red' }}>{error}</div>}
            </div>

            {jobs.length === 0 ? (
                <div style={{ textAlign: 'center', color: '#999', padding: '1rem' }}>No jobs yet. Click "Scrape jobs" to search.</div>
            ) : (
                <div className="job-list-container">
                    {jobs.map((j) => (
                        <div key={j.id || j.url} style={{ minWidth: '250px', width: '250px', flexShrink: 0 }}>
                            <JobCard
                                job={j}
                                onSelect={() => {}}
                                onTailor={onTailor}
                                onIgnore={onIgnore}
                            />
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}