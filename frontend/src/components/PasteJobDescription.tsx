import { useState } from "react";
import type { Job } from "../types";

type Props = {
  onTailor: (job: Job) => void;
};

export default function PasteJobDescription({ onTailor }: Props) {
  const [pasted, setPasted] = useState("");

  function handleUse() {
    const text = pasted.trim();
    if (!text) return;

    const dummyJob: Job = {
      id: `pasted-${Date.now()}`,
      title: "Pasted job description",
      description: text,
      url: "about:blank",
    };
    onTailor(dummyJob);
  }

  return (
    <div className="paste-job">
      <label>Or paste a job description:</label>
      <textarea
        value={pasted}
        onChange={(e) => setPasted(e.target.value)}
        placeholder="Paste job description here..."
        rows={6}
      />
      <button
        type="button"
        className="paste-job-btn"
        onClick={handleUse}
        disabled={!pasted.trim()}
      >
        Use this description
      </button>
    </div>
  );
}
