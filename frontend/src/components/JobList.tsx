import { useState, useEffect } from "react";
import JobCard from "./JobCard";
import type { Job } from '../types'
import { fetchJobs } from '../api/jobs';

type SelectorPayload = { type: string; intern: boolean; fullTime: boolean };

type Props = {
  query?: SelectorPayload;
  onTailor?: (job: Job) => void;
  onIgnore?: (job: Job) => void;
  token?: string | null;
  /** When this changes, re-run scrape (e.g. after user ignores a job). */
  refreshTrigger?: number;
}

export default function JobList( { query, onTailor, onIgnore, token, refreshTrigger }: Props ) {
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

    useEffect(() => {
        if (query && refreshTrigger != null && refreshTrigger > 0) {
            onScrape();
        }
    }, [refreshTrigger]);

    return (
        <div className="job-list">
            <div className="job-list-toolbar">
                <button onClick={onScrape} disabled={loading}>{loading ? 'Searching…' : 'Scrape jobs'}</button>
                {error && <div className="job-list-error">{error}</div>}
            </div>

            {jobs.length === 0 ? (
                <div className="job-list-empty">No jobs yet. Click "Scrape jobs" to search.</div>
            ) : (
                <div className="job-list-container">
                    {jobs.map((j) => (
                        <div key={j.id || j.url} className="job-list-card-wrapper">
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