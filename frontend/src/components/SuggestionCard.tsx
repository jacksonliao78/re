import type { Suggestion, Resume } from '../types'
import { useState, useEffect } from "react";
import { applySuggestion, validSuggestion } from '../utils/editResume';
import '../App.css';

type Props = {
    suggestion: Suggestion;
    resume: Resume;
    onApply?: (suggestion: Suggestion) => void;
    onReject?: (suggestion: Suggestion) => void;
    onResumeUpdate?: (updatedResume: Resume) => void;
    isApplied?: boolean;
    isRejected?: boolean;
}

export default function SuggestionCard( { suggestion, resume, onApply, onReject, onResumeUpdate,isApplied = false,isRejected = false }: Props ) {
    const [localApplied, setLocalApplied] = useState(isApplied);
    const [localRejected, setLocalRejected] = useState(isRejected);
    const [isValid, setIsValid] = useState(true);

    // validate suggestion when resume changes
    useEffect(() => {
        setIsValid(validSuggestion(resume, suggestion));
    }, [resume, suggestion]);

    // sync with prop changes
    useEffect(() => {
        setLocalApplied(isApplied);
    }, [isApplied]);

    useEffect(() => {
        setLocalRejected(isRejected);
    }, [isRejected]);

    function handleApply() {
        if (!isValid || localApplied || localRejected) return;

        const updatedResume = applySuggestion(resume, suggestion);
        setLocalApplied(true);
        

        onApply?.(suggestion);
        onResumeUpdate?.(updatedResume);
    }

    function handleReject() {
        if (localRejected) return;

        setLocalRejected(true);
        onReject?.(suggestion);
    }

    // don't render if rejected
    if (localRejected) {
        return null;
    }

    const sectionLabel = suggestion.section.charAt(0).toUpperCase() + suggestion.section.slice(1);
    const contextInfo = suggestion.entryIdx !== undefined 
        ? `Entry ${suggestion.entryIdx}${suggestion.bulletIdx !== undefined ? `, Bullet ${suggestion.bulletIdx}` : ''}`
        : '';

    return (
        <article className="suggestion-card">
            <div className="suggestion-header">
                <span className="suggestion-section">{sectionLabel}</span>
                {contextInfo && <span className="suggestion-context">{contextInfo}</span>}
                {localApplied && <span className="suggestion-status applied">✓ Applied</span>}
                {!isValid && <span className="suggestion-status invalid">⚠ Invalid</span>}
            </div>

            <div className="suggestion-content">
                <div className="suggestion-original">
                    <strong>Original:</strong>
                    <p>{suggestion.original}</p>
                </div>

                <div className="suggestion-arrow">→</div>

                <div className="suggestion-updated">
                    <strong>Updated:</strong>
                    <p>{suggestion.updated}</p>
                </div>
            </div>

            {suggestion.explanation && (
                <div className="suggestion-explanation">
                    <strong>Explanation:</strong>
                    <p>{suggestion.explanation}</p>
                </div>
            )}

            <div className="suggestion-actions">
                <button 
                    onClick={handleApply} 
                    disabled={localApplied || !isValid || localRejected}
                    className="suggestion-btn apply-btn"
                >
                    {localApplied ? 'Applied ✓' : 'Apply'}
                </button>
                <button 
                    onClick={handleReject} 
                    disabled={localApplied || localRejected}
                    className="suggestion-btn reject-btn"
                >
                    Reject
                </button>
            </div>
        </article>
    );
}