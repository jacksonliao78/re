import { useState, useEffect } from "react";
import "./App.css";
import ResumeUploader from "./components/ResumeUploader";
import JobSelector from "./components/JobSelector";
import JobList from "./components/JobList";
import PasteJobDescription from "./components/PasteJobDescription";
import SuggestionList from "./components/SuggestionList";
import ResumeEditor from "./components/ResumeEditor";
import Login from "./components/Login";
import Register from "./components/Register";
import { useAuth } from "./contexts/AuthContext";
import { getDefaultResume, addIgnoredJob, saveDefaultResume } from "./api/auth";
import type { Resume, Job } from "./types";
import { saveResume } from "./utils/resumeStorage";

function App() {
  const { isAuthenticated, token, isLoading, logout } = useAuth();
  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [query, setQuery] = useState<{ type: string; intern: boolean; fullTime: boolean } | undefined>(undefined);
  const [originalResume, setOriginalResume] = useState<Resume | null>(null);
  const [resume, setResume] = useState<Resume | null>(null);
  const [jobForTailoring, setJobForTailoring] = useState<Job | null>(null);

  // Load default resume when user logs in
  useEffect(() => {
    if (!isAuthenticated || !token) return;
    getDefaultResume(token)
      .then((r) => {
        if (r) {
          setOriginalResume(r);
          setResume(r);
          saveResume(r);
        }
      })
      .catch(() => {});
  }, [isAuthenticated, token]);

  function handleNewResume(newResume: Resume | null) {
    setOriginalResume(newResume);
    setResume(newResume);
    if (newResume) saveResume(newResume);
    setJobForTailoring(null);
  }

  function handleResumeUpdateFromSuggestions(updatedResume: Resume) {
    setResume(updatedResume);
  }

  function handleTailor(job: Job) {
    if (originalResume) setResume(originalResume);
    setJobForTailoring(job);
  }

  async function handleIgnoreOrComplete(job: Job) {
    if (token) {
      try {
        await addIgnoredJob(job.id || job.url, token);
      } catch (_) {}
    }
    setJobForTailoring(null);
  }

  if (isLoading) {
    return (
      <div className="app-root" style={{ justifyContent: "center", alignItems: "center" }}>
        <p>Loading…</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="app-root">
        {authMode === "login" ? (
          <Login onSwitchToRegister={() => setAuthMode("register")} />
        ) : (
          <Register onSwitchToLogin={() => setAuthMode("login")} />
        )}
      </div>
    );
  }

  return (
    <div className="app-root">
      <header className="app-header">
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%" }}>
          <h1 style={{ margin: 0 }}>get a job</h1>
          <button type="button" onClick={logout} className="clear-btn">Log out</button>
        </div>
        <ResumeUploader
          onResumeChange={handleNewResume}
          resume={resume}
          originalResume={originalResume}
          onSaveDefault={token && originalResume ? () => saveDefaultResume(originalResume, token) : undefined}
        />
      </header>

      <main className="app-main">
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
            />
            <PasteJobDescription onTailor={handleTailor} />
          </div>
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
                key={jobForTailoring.id || jobForTailoring.url}
                resume={resume}
                job={jobForTailoring}
                onResumeUpdate={handleResumeUpdateFromSuggestions}
                onComplete={handleIgnoreOrComplete}
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