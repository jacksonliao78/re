import { useCallback, useEffect, useRef, useState } from "react";
import {
  createKnowledgeDocument,
  deleteKnowledgeDocument,
  getKnowledgeDocumentById,
  getKnowledgeDocuments,
} from "../api/resume";
import type { KnowledgeDocument, KnowledgeDocumentDetail } from "../types";

type Props = {
  token: string | null;
};

function getErrorMessage(err: unknown, fallback: string) {
  if (err instanceof Error && err.message) return err.message;
  return fallback;
}

export default function KnowledgePanel({ token }: Props) {
  const [docs, setDocs] = useState<KnowledgeDocument[]>([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [openEntryId, setOpenEntryId] = useState<string | null>(null);
  const [openEntry, setOpenEntry] = useState<KnowledgeDocumentDetail | null>(null);
  const [entryLoading, setEntryLoading] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const openRequestSeq = useRef(0);

  const loadDocuments = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const data = (await getKnowledgeDocuments(token)) as KnowledgeDocument[];
      setDocs(Array.isArray(data) ? data : []);
    } catch (err: unknown) {
      setError(getErrorMessage(err, "Failed to load saved context."));
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  async function handleOpenEntry(id: string) {
    if (!token) return;
    const requestId = ++openRequestSeq.current;
    setOpenEntryId(id);
    setOpenEntry(null);
    setEntryLoading(true);
    setError(null);
    setStatus(null);
    try {
      const detail = (await getKnowledgeDocumentById(id, token)) as KnowledgeDocumentDetail;
      if (requestId !== openRequestSeq.current) return;
      setOpenEntry(detail);
    } catch (err: unknown) {
      if (requestId !== openRequestSeq.current) return;
      setError(getErrorMessage(err, "Failed to load this context item."));
      setOpenEntryId(null);
    } finally {
      if (requestId !== openRequestSeq.current) return;
      setEntryLoading(false);
    }
  }

  async function handleDeleteEntry(id: string) {
    if (!token) return;
    const confirmed = window.confirm("Delete this saved context item? This cannot be undone.");
    if (!confirmed) return;
    setDeletingId(id);
    setError(null);
    setStatus(null);
    try {
      await deleteKnowledgeDocument(id, token);
      setDocs((prev) => prev.filter((doc) => doc.id !== id));
      if (openEntryId === id) {
        openRequestSeq.current += 1;
        setOpenEntryId(null);
        setOpenEntry(null);
        setEntryLoading(false);
      }
      setStatus("Context item deleted.");
    } catch (err: unknown) {
      setError(getErrorMessage(err, "Failed to delete this context item."));
    } finally {
      setDeletingId(null);
    }
  }

  async function handleAddKnowledge() {
    if (!token) return;
    if (!title.trim() || !content.trim()) {
      setError("Title and content are required.");
      return;
    }
    setSaving(true);
    setError(null);
    setStatus(null);
    try {
      await createKnowledgeDocument(
        {
          title: title.trim(),
          content: content.trim(),
          sourceType: "note",
        },
        token
      );
      setTitle("");
      setContent("");
      setStatus("Context saved.");
      await loadDocuments();
    } catch (err: unknown) {
      setError(getErrorMessage(err, "Failed to save context."));
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="knowledge-panel">
      <h3>More context for better tailoring</h3>
      {!token ? (
        <div className="upload-status">Sign in to save extra context for more accurate tailoring.</div>
      ) : (
        <>
          <p className="upload-status">
            Add details about your experience, projects, outcomes, and tools so the system can tailor suggestions more accurately.
          </p>

          <div className="knowledge-form">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Title (for example: Backend Internship)"
            />
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Paste details, bullets, metrics, technologies, and accomplishments you want considered."
              rows={5}
            />
            <button type="button" onClick={handleAddKnowledge} disabled={saving}>
              {saving ? "Saving..." : "Add context"}
            </button>
          </div>

          {loading && <div className="upload-status">Loading saved context...</div>}
          {status && <div className="upload-status">{status}</div>}
          {error && <div className="upload-error">{error}</div>}

          <div className="knowledge-list">
            {docs.length === 0 ? (
              <div className="upload-status">No saved context yet.</div>
            ) : (
              docs.map((doc) => (
                <div key={doc.id} className="knowledge-item">
                  <div className="knowledge-item-top">
                    <div>
                      <div className="knowledge-item-title">{doc.title}</div>
                      <div className="knowledge-item-meta">{doc.chunkCount} saved sections</div>
                    </div>
                    <div className="knowledge-item-actions">
                      <button
                        type="button"
                        className="knowledge-action-button"
                        onClick={() => handleOpenEntry(doc.id)}
                        disabled={entryLoading && openEntryId === doc.id}
                      >
                        {entryLoading && openEntryId === doc.id ? "Opening..." : "Open"}
                      </button>
                      <button
                        type="button"
                        className="knowledge-action-button knowledge-delete-button"
                        onClick={() => handleDeleteEntry(doc.id)}
                        disabled={deletingId === doc.id}
                      >
                        {deletingId === doc.id ? "Deleting..." : "Delete"}
                      </button>
                    </div>
                  </div>
                  {openEntryId === doc.id && (
                    <div className="knowledge-item-content">
                      {entryLoading ? "Loading content..." : openEntry?.content || "No content available."}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
