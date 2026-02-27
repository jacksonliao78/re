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
    <div className="paste-job" style={{ marginTop: "1.5rem" }}>
      <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 600 }}>
        Or paste a job description:
      </label>
      <textarea
        value={pasted}
        onChange={(e) => setPasted(e.target.value)}
        placeholder="Paste job description here..."
        rows={6}
        style={{
          width: "100%",
          padding: "0.75rem",
          borderRadius: "6px",
          border: "1px solid #e6e6e6",
          fontSize: "0.9rem",
          resize: "vertical",
          boxSizing: "border-box",
        }}
      />
      <button
        type="button"
        onClick={handleUse}
        disabled={!pasted.trim()}
        style={{
          marginTop: "0.5rem",
          padding: "0.5rem 1rem",
          background: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: pasted.trim() ? "pointer" : "not-allowed",
          opacity: pasted.trim() ? 1 : 0.6
        }}
      >
        Use this description
      </button>
    </div>
  );
}
