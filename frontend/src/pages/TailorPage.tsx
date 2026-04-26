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
      } catch (_) {}
    }
    setJobForTailoring(null);
  }

  return (
    <div className="tailor-page">
      <section className="job-scrape-section">
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
        <div className="job-paste-section">
          <PasteJobDescription onTailor={handleTailor} />
        </div>
      </section>

      <section className="tailor-content">
        <div className="tailor-viewer">
          {resume ? (
            <ResumeViewer resume={resume} />
          ) : (
            <div className="editor-placeholder">
              Upload a resume first to tailor it.
            </div>
          )}
        </div>

        <aside className="tailor-suggestions">
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
      </section>
    </div>
  );
}
