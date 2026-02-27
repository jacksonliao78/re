import React, { useState, useRef, useEffect } from "react";
import { uploadResume } from "../api/resume";
import type { Resume } from "../types";
import { saveResume, loadResume, clearResume } from "../utils/resumeStorage";
import "../App.css";

type Props = {
  resume?: Resume | null;
  originalResume?: Resume | null;
  onResumeChange?: (resume: Resume | null) => void;
  /** When set, show "Save as default" and call this to store the current default (original) resume */
  onSaveDefault?: () => void | Promise<void>;
}

export default function ResumeUploader({ resume: propResume, originalResume, onResumeChange, onSaveDefault }: Props = {}) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [resume, setResume] = useState<Resume | null>(propResume || null);
  const [error, setError] = useState<string | null>(null);
  const [loadedFromStorage, setLoadedFromStorage] = useState(false);
  const [savingDefault, setSavingDefault] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);

  // sync with prop changes
  useEffect(() => {
    if (propResume !== undefined) {
      setResume(propResume);
    }
  }, [propResume]);

  // load Resume from local storage if possible
  useEffect(() => {
    if (propResume === undefined) {
      const savedResume = loadResume();
      if (savedResume) {
        setResume(savedResume);
        setLoadedFromStorage(true);
        onResumeChange?.(savedResume);
      }
    }
  }, [propResume, onResumeChange]);

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
    setResume(null);
    setError(null);
    setLoadedFromStorage(false);
    try {
      const res = await uploadResume(file);
      if (res.ok && res.data) {
        const newResume = res.data as Resume;
        setResume(newResume);
        saveResume(newResume);
        onResumeChange?.(newResume);
      } else {
        setError(res.data?.message || "Failed to upload resume");
      }
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  function handleClearResume() {
    setResume(null);
    setFile(null);
    setError(null);
    setLoadedFromStorage(false);
    clearResume();
    onResumeChange?.(null);
    if (inputRef.current) {
      inputRef.current.value = "";
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
        {resume && (
          <button onClick={handleClearResume} className="clear-btn" style={{ marginLeft: "0.5rem" }}>
            Clear Resume
          </button>
        )}
        {onSaveDefault && originalResume && (
          <button
            type="button"
            onClick={async () => {
              setSavingDefault(true);
              try {
                await onSaveDefault();
              } finally {
                setSavingDefault(false);
              }
            }}
            disabled={savingDefault}
            style={{ marginLeft: "0.5rem" }}
          >
            {savingDefault ? "Saving…" : "Save as default resume"}
          </button>
        )}
      </div>

      {loadedFromStorage && resume && (
        <div style={{ marginTop: "0.5rem", fontSize: "0.9rem", color: "#666" }}>
          Resume loaded from previous session
        </div>
      )}

      {error && (
        <div className="upload-error" style={{ color: "red", marginTop: "1rem" }}>
          {error}
        </div>
      )}

    </div>
  );
}
