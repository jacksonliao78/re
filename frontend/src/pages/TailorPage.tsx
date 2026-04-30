import { useState } from "react";
import JobSelector from "../components/JobSelector";
import JobList from "../components/JobList";
import PasteJobDescription from "../components/PasteJobDescription";
import SuggestionList from "../components/SuggestionList";
import ResumeViewer from "../components/ResumeViewer";
import { useResume } from "../contexts/ResumeContext";
import { useAuth } from "../contexts/AuthContext";
import { addIgnoredJob } from "../api/auth";
import type { Job } from "../types";

export default function TailorPage() {
  const { resume, originalResume, setResume } = useResume();
  const { token } = useAuth();

  const [refreshJobsKey, setRefreshJobsKey] = useState(0);
  const [query, setQuery] = useState<
    { type: string; intern: boolean; fullTime: boolean } | undefined
  >(undefined);
  const [jobForTailoring, setJobForTailoring] = useState<Job | null>(null);

  function handleTailor(job: Job) {
    if (originalResume) setResume(originalResume);
    setJobForTailoring(job);
  }

  async function handleIgnoreOrComplete(job: Job) {
    if (token) {
      try {
        await addIgnoredJob(job.id || job.url, token);
        setRefreshJobsKey((k) => k + 1);
      } catch {
        // Keep the tailoring flow moving if saving the ignored job fails.
      }
    }
    setJobForTailoring(null);
  }

  const selectedJobMeta = jobForTailoring
    ? [jobForTailoring.company, jobForTailoring.location].filter(Boolean).join(" - ")
    : "";

  return (
    <div className="tailor-page">
      <header className="tailor-page-header">
        <h2>Tailor your resume</h2>
        <p>Choose a job, review your resume, then apply targeted suggestions.</p>
      </header>

      <div className="tailor-workspace">
        <section className="tailor-source-panel" aria-label="Job and input source">
          <div className="panel-heading">
            <h3>Job source</h3>
            <p>Scrape jobs or paste a description to begin tailoring.</p>
          </div>

          <div className="job-scrape-section">
            <div className="job-scrape-header">
              <JobSelector onChange={(q) => setQuery(q)} />
            </div>
            <div className="job-scrape-body">
              <JobList
                query={query}
                onTailor={handleTailor}
                onIgnore={handleIgnoreOrComplete}
                token={token}
                refreshTrigger={refreshJobsKey}
              />
            </div>
          </div>

          <div className="job-paste-section">
            <PasteJobDescription onTailor={handleTailor} />
          </div>
        </section>

        <section className="tailor-preview-panel" aria-label="Resume preview">
          <div className="panel-heading">
            <h3>Resume preview</h3>
            <p>Suggestions update this preview as you apply them.</p>
          </div>
          {resume ? (
            <ResumeViewer resume={resume} />
          ) : (
            <div className="editor-placeholder">
              Upload a resume first to tailor it.
            </div>
          )}
        </section>

        <aside className="tailor-action-panel" aria-label="Suggestions and actions">
          <div className="panel-heading">
            <h3>Suggestions</h3>
            <p>Generate and apply updates for the selected job.</p>
          </div>

          {jobForTailoring && (
            <div className="selected-job-summary">
              <div className="selected-job-label">Selected job</div>
              <strong>{jobForTailoring.title}</strong>
              {selectedJobMeta && <span>{selectedJobMeta}</span>}
            </div>
          )}

          {jobForTailoring ? (
            <SuggestionList
              key={jobForTailoring.id || jobForTailoring.url}
              resume={resume}
              job={jobForTailoring}
              token={token}
              onResumeUpdate={setResume}
              onComplete={handleIgnoreOrComplete}
            />
          ) : (
            <div className="suggestions-placeholder">
              Select a job and click "Tailor" to see suggestions
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}
