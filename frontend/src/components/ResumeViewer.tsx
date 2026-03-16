import { useEffect, useState } from "react";
import type { Resume } from "../types";

type Props = {
  resume: Resume | null;
  className?: string;
};

export default function ResumeViewer({ resume, className = "" }: Props) {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let revokedUrl: string | null = null;

    async function fetchPdf() {
      if (!resume) {
        setPdfUrl(null);
        setError(null);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const resp = await fetch("/resume/render-pdf", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(resume),
        });
        if (!resp.ok) {
          const text = await resp.text();
          throw new Error(`Failed to render PDF: ${resp.status} ${text}`);
        }
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        revokedUrl = url;
        setPdfUrl(url);
      } catch (err: any) {
        setError(err?.message || "Failed to render resume PDF");
        setPdfUrl(null);
      } finally {
        setLoading(false);
      }
    }

    fetchPdf();

    return () => {
      if (revokedUrl) {
        URL.revokeObjectURL(revokedUrl);
      }
    };
  }, [resume]);

  return (
    <div className={`resume-viewer ${className}`}>
      {loading && <div className="resume-editor-loading">Rendering resume PDF…</div>}
      {error && (
        <div className="resume-editor-error">
          {error}
        </div>
      )}
      {!loading && !error && !pdfUrl && (
        <div className="editor-placeholder">
          Upload a resume to see it rendered here.
        </div>
      )}
      {pdfUrl && !loading && !error && (
        <object
          data={pdfUrl}
          type="application/pdf"
          width="100%"
          height="100%"
        >
          <p>
            Your browser does not support embedded PDFs.{" "}
            <a href={pdfUrl} target="_blank" rel="noreferrer">
              Open the PDF in a new tab.
            </a>
          </p>
        </object>
      )}
    </div>
  );
}

