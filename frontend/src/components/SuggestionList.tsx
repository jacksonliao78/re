import { useState, useEffect } from "react";
import SuggestionCard from "./SuggestionCard";
import { getSuggestions } from "../api/tailor";
import type { Suggestion, Resume, Job } from "../types";
import "../App.css";

type Props = {
    resume: Resume | null;
    job: Job | null;
    onResumeUpdate?: (updatedResume: Resume) => void;
}

export default function SuggestionList({ resume, job, onResumeUpdate }: Props) {
    const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [appliedIds, setAppliedIds] = useState<Set<string>>(new Set());
    const [rejectedIds, setRejectedIds] = useState<Set<string>>(new Set());
    
    // track current resume to ensure we always use the latest version
    const [currentResume, setCurrentResume] = useState<Resume | null>(resume);
    
    // update  when prop changes
    useEffect(() => {
        setCurrentResume(resume);
    }, [resume]);

    async function handleFetchSuggestions() {
        if (!currentResume || !job) {
            setError("Resume and job are required to generate suggestions");
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const fetched = await getSuggestions(currentResume, job);
            setSuggestions(fetched);

            // reset with new list
            setAppliedIds(new Set());
            setRejectedIds(new Set());
        } catch (err: any) {
            setError(err?.message || "Failed to fetch suggestions");
            console.error("Error fetching suggestions:", err);
        } finally {
            setLoading(false);
        }
    }

    function handleApply(suggestion: Suggestion) {
        const suggestionId = `${suggestion.section}-${suggestion.entryIdx ?? 'none'}-${suggestion.bulletIdx ?? 'none'}`;
        setAppliedIds(new Set([...appliedIds, suggestionId]));
    }

    function handleReject(suggestion: Suggestion) {
        const suggestionId = `${suggestion.section}-${suggestion.entryIdx ?? 'none'}-${suggestion.bulletIdx ?? 'none'}`;
        setRejectedIds(new Set([...rejectedIds, suggestionId]));
    }

    function handleResumeUpdate(updatedResume: Resume) {
        setCurrentResume(updatedResume);
        onResumeUpdate?.(updatedResume);
    }

    // filter rejected suggestions
    const visibleSuggestions = suggestions.filter(s => {
        const suggestionId = `${s.section}-${s.entryIdx ?? 'none'}-${s.bulletIdx ?? 'none'}`;
        return !rejectedIds.has(suggestionId);
    });

    if (!currentResume || !job) {
        return (
            <div className="suggestion-list">
                <div className="suggestion-list-empty">
                    Upload a resume and select a job to generate suggestions.
                </div>
            </div>
        );
    }

    return (
        <div className="suggestion-list">
            <div className="suggestion-list-header">
                <h3>Suggestions for {job.title}</h3>
                {suggestions.length > 0 && (
                    <span className="suggestion-list-stats">
                        {visibleSuggestions.length} available
                        {appliedIds.size > 0 && ` • ${appliedIds.size} applied`}
                    </span>
                )}
            </div>

            {suggestions.length === 0 && !loading && !error && (
                <div className="suggestion-list-actions">
                    <button 
                        onClick={handleFetchSuggestions} 
                        className="suggestion-fetch-btn"
                        disabled={loading}
                    >
                        Generate Suggestions
                    </button>
                </div>
            )}

            {loading && (
                <div className="suggestion-list-loading">Loading suggestions...</div>
            )}

            {error && (
                <div className="suggestion-list-error">
                    Error: {error}
                    <button 
                        onClick={handleFetchSuggestions} 
                        className="suggestion-retry-btn"
                        style={{ marginTop: "0.5rem" }}
                    >
                        Retry
                    </button>
                </div>
            )}

            {suggestions.length > 0 && visibleSuggestions.length === 0 && (
                <div className="suggestion-list-empty">
                    All suggestions have been applied or rejected.
                </div>
            )}

            {visibleSuggestions.length > 0 && (
                <div className="suggestion-list-content">
                    {visibleSuggestions.map((suggestion, index) => {
                        const suggestionId = `${suggestion.section}-${suggestion.entryIdx ?? 'none'}-${suggestion.bulletIdx ?? 'none'}`;
                        return (
                            <SuggestionCard
                                key={`${suggestionId}-${index}`}
                                suggestion={suggestion}
                                resume={currentResume}
                                onApply={handleApply}
                                onReject={handleReject}
                                onResumeUpdate={handleResumeUpdate}
                                isApplied={appliedIds.has(suggestionId)}
                                isRejected={rejectedIds.has(suggestionId)}
                            />
                        );
                    })}
                </div>
            )}
        </div>
    );
}
