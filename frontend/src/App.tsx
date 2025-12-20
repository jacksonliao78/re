import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import ResumeUploader from "./components/ResumeUploader";
import JobSelector from "./components/JobSelector";
import JobList from "./components/JobList";

function App() {
  const [count, setCount] = useState(0);
  const [query, setQuery] = useState<{ type: string; intern: boolean; fullTime: boolean } | undefined>(undefined);

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
          <ResumeUploader />
        </section>

        <aside className="right-pane">
          <div className="card">
            <button onClick={() => setCount((c) => c + 1)}>
              count is {count}
            </button>
            <p>Edit <code>src/App.tsx</code> and save to test HMR</p>
          </div>

          <div style={{ marginTop: 12 }}>
            <JobList query={query} />
          </div>
        </aside>
      </main>
    </div>
  );
}

export default App;