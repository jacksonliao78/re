import React, { useState } from "react";
import type { Job } from "../types"

type Props = {
    job: Job;
    onSelect ?: (jobId?: string) => void;
    onTailor?: (jobId?: string) => void;
}

export default function JobCard( { job, onSelect, onTailor }: Props ) {
    const [selected, setSelected] = useState(false);

    function handleSelect() {
        const next = !selected;
        setSelected(next);
        onSelect?.(job.id);
    }

    function handleTailor(e: React.MouseEvent) {
        e.stopPropagation();
        onTailor?.(job.id) ?? onSelect?.(job.id);
    }

    return (
        <article className={`job-card ${selected ? 'selected' : ''}`} onClick={handleSelect}>
            <h4 className="job-title">{job.title}</h4>
            <div className="job-meta">{job.company}{job.location ? ` — ${job.location}` : ''}</div>
            {job.description && <p className="job-desc">{job.description}</p>}
            <div className="job-actions">
                <button onClick={(e) => { e.stopPropagation(); handleSelect(); }}>{selected ? 'Deselect' : 'Select'}</button>
                {selected && (
                    <button onClick={handleTailor} className="tailor-btn">Tailor</button>
                )}
                {job.url && (
                <a href={job.url} target="_blank" rel="noreferrer">View</a>
                )}
            </div>
        </article>
    )

}
