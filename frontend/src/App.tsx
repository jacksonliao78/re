import { useState } from "react";
import "./App.css";
import ResumeUploader from "./components/ResumeUploader";
import JobSelector from "./components/JobSelector";
import JobList from "./components/JobList";
import SuggestionList from "./components/SuggestionList";
import ResumeEditor from "./components/ResumeEditor";
import type { Resume, Job } from "./types";
import { saveResume } from "./utils/resumeStorage";

function App() {
  const [query, setQuery] = useState<{ type: string; intern: boolean; fullTime: boolean } | undefined>(undefined);
  const [resume, setResume] = useState<Resume | null>(null);
  const [jobForTailoring, setJobForTailoring] = useState<Job | null>(null);

  function handleResumeUpdate(updatedResume: Resume) {
    setResume(updatedResume);
    saveResume(updatedResume);
  }

  function handleTailor(job: Job) {
    setJobForTailoring(job);
  }

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Resume Tailoring</h1>
        <ResumeUploader onResumeChange={setResume} resume={resume} />
        <JobSelector onChange={(q) => setQuery(q)} />
      </header>

      <main className="app-main">
        <section className="job-list-section">
          <JobList query={query} onTailor={handleTailor} />
        </section>

        <section className="content-section">
          <div className="editor-pane">
            {resume ? (
              <ResumeEditor resume={resume} editable={false} />
            ) : (
              <div className="editor-placeholder">
                Upload a resume to see it here
              </div>
            )}
          </div>

          <aside className="suggestions-pane">
            {jobForTailoring && (
              <SuggestionList 
                resume={resume} 
                job={jobForTailoring}
                onResumeUpdate={handleResumeUpdate}
              />
            )}
            {!jobForTailoring && (
              <div className="suggestions-placeholder">
                Select a job and click "Tailor" to see suggestions
              </div>
            )}
          </aside>
        </section>
      </main>
    </div>
  );
}

export default App;