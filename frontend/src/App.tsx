import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import ResumeUploader from "./components/ResumeUploader";
import JobSelector from "./components/JobSelector";
import JobList from "./components/JobList";
import SuggestionList from "./components/SuggestionList";
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
        <div>
          <a href="https://vite.dev" target="_blank" rel="noreferrer">
            <img src={viteLogo} className="logo" alt="Vite logo" />
          </a>
          <a href="https://react.dev" target="_blank" rel="noreferrer">
            <img src={reactLogo} className="logo react" alt="React logo" />
          </a>
        </div>
        <h1>Resume </h1>
      </header>

      <main className="app-main">
        <section className="left-pane">
          <JobSelector onChange={(q) => setQuery(q)} />
          <ResumeUploader onResumeChange={setResume} resume={resume} />
        </section>

        <aside className="right-pane">
          <div style={{ marginTop: 12 }}>
            <JobList query={query} onTailor={handleTailor} />
          </div>
          {jobForTailoring && (
            <div style={{ marginTop: 24 }}>
              <SuggestionList 
                resume={resume} 
                job={jobForTailoring}
                onResumeUpdate={handleResumeUpdate}
              />
            </div>
          )}
        </aside>
      </main>
  
    </div>
  );
}

export default App;