import React, { useState, useRef } from "react";
import { uploadResume } from "../api/resume";
import "../App.css";

export default function ResumeUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  function onDrop(e: React.DragEvent) {
    e.preventDefault();
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) setFile(f);
  }

  function onDragOver(e: React.DragEvent) {
    e.preventDefault();
  }

  function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files && e.target.files[0];
    if (f) setFile(f);
  }

  async function onSubmit() {
    if (!file) return alert("Please select a PDF file first.");
    setLoading(true);
    setResult(null);
    try {
      const res = await uploadResume(file);
      setResult(res);
    } catch (err) {
      setResult({ ok: false, error: String(err) });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="uploader">
      <h2>Upload resume</h2>

      <div
        className="dropzone"
        onDrop={onDrop}
        onDragOver={onDragOver}
        onClick={() => inputRef.current && inputRef.current.click()}
        role="button"
      >
        {file ? (
          <div className="file-name">{file.name}</div>
        ) : (
          <div className="drop-instructions">Drop PDF here or click to browse</div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          onChange={onFileChange}
          style={{ display: "none" }}
        />
      </div>

      <div className="controls">
        <button onClick={onSubmit} disabled={loading} className="upload-btn">
          {loading ? "Uploading…" : "Upload"}
        </button>
      </div>

      <div className="result">
        <h3>Result</h3>
        <pre>{result ? JSON.stringify(result, null, 2) : "No result yet."}</pre>
      </div>
    </div>
  );
}
