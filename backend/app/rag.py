import math
import uuid
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import UserKnowledgeDocument, UserKnowledgeChunk
from app.llm import get_embeddings_model


class KnowledgeStoreUnavailableError(RuntimeError):
    pass


def _chunk_text(content: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:
    text = (content or "").strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(0, end - overlap)
    return [c for c in chunks if c]


def _fallback_embedding(text: str, dims: int = 64) -> list[float]:
    vec = [0.0] * dims
    for i, ch in enumerate(text.lower()):
        vec[(ord(ch) + i) % dims] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def _embed_text(text: str) -> list[float]:
    emb = get_embeddings_model()
    if emb is None:
        return _fallback_embedding(text)
    try:
        values = emb.embed_query(text)
        if not isinstance(values, list) or not values:
            return _fallback_embedding(text)
        norm = math.sqrt(sum(float(v) * float(v) for v in values)) or 1.0
        return [float(v) / norm for v in values]
    except Exception:
        return _fallback_embedding(text)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    size = min(len(a), len(b))
    if size == 0:
        return 0.0
    return sum(a[i] * b[i] for i in range(size))


def ingest_user_knowledge(
    db: Session,
    user_id: uuid.UUID,
    title: str,
    content: str,
    source_type: str = "note",
) -> tuple[UserKnowledgeDocument, int]:
    try:
        doc = UserKnowledgeDocument(
            user_id=user_id,
            title=(title or "Untitled").strip()[:256] or "Untitled",
            source_type=(source_type or "note").strip()[:64] or "note",
            content=content or "",
        )
        db.add(doc)
        db.flush()

        chunks = _chunk_text(content)
        rows: list[UserKnowledgeChunk] = []
        for idx, chunk in enumerate(chunks):
            rows.append(
                UserKnowledgeChunk(
                    document_id=doc.id,
                    user_id=user_id,
                    chunk_index=idx,
                    text=chunk,
                    metadata_json={"title": doc.title, "source_type": doc.source_type},
                    embedding=_embed_text(chunk),
                )
            )
        if rows:
            db.bulk_save_objects(rows)
        db.commit()
        db.refresh(doc)
        return doc, len(rows)
    except SQLAlchemyError as exc:
        db.rollback()
        raise KnowledgeStoreUnavailableError("knowledge store unavailable") from exc


def retrieve_relevant_chunks(
    db: Session,
    user_id: uuid.UUID,
    query_text: str,
    top_k: int = 8,
) -> list[dict[str, Any]]:
    q_vec = _embed_text(query_text)
    try:
        chunks = (
            db.query(UserKnowledgeChunk).filter(UserKnowledgeChunk.user_id == user_id).all()
        )
    except SQLAlchemyError as exc:
        raise KnowledgeStoreUnavailableError("knowledge store unavailable") from exc
    scored: list[tuple[float, UserKnowledgeChunk]] = []
    for c in chunks:
        emb = c.embedding if isinstance(c.embedding, list) else []
        score = _cosine_similarity(q_vec, [float(v) for v in emb]) if emb else 0.0
        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    out: list[dict[str, Any]] = []
    for score, c in scored[:max(1, top_k)]:
        out.append(
            {
                "chunkId": str(c.id),
                "documentId": str(c.document_id),
                "chunkIndex": c.chunk_index,
                "score": round(float(score), 5),
                "text": c.text,
                "metadata": c.metadata_json or {},
            }
        )
    return out


def list_user_knowledge_documents(db: Session, user_id: uuid.UUID) -> list[dict[str, Any]]:
    try:
        docs = (
            db.query(UserKnowledgeDocument)
            .filter(UserKnowledgeDocument.user_id == user_id)
            .order_by(UserKnowledgeDocument.created_at.desc())
            .all()
        )
        counts: dict[str, int] = {}
        for d in docs:
            counts[str(d.id)] = (
                db.query(UserKnowledgeChunk)
                .filter(UserKnowledgeChunk.document_id == d.id)
                .count()
            )

        return [
            {
                "id": str(d.id),
                "title": d.title,
                "sourceType": d.source_type,
                "chunkCount": counts.get(str(d.id), 0),
            }
            for d in docs
        ]
    except SQLAlchemyError as exc:
        raise KnowledgeStoreUnavailableError("knowledge store unavailable") from exc


def get_user_knowledge_document(
    db: Session, user_id: uuid.UUID, doc_id: str | uuid.UUID
) -> dict[str, Any] | None:
    try:
        parsed_doc_id = doc_id if isinstance(doc_id, uuid.UUID) else uuid.UUID(str(doc_id))
    except (ValueError, TypeError):
        return None

    try:
        doc = (
            db.query(UserKnowledgeDocument)
            .filter(
                UserKnowledgeDocument.id == parsed_doc_id,
                UserKnowledgeDocument.user_id == user_id,
            )
            .first()
        )
        if doc is None:
            return None

        chunk_count = (
            db.query(UserKnowledgeChunk)
            .filter(UserKnowledgeChunk.document_id == doc.id)
            .count()
        )
        return {
            "id": str(doc.id),
            "title": doc.title,
            "sourceType": doc.source_type,
            "content": doc.content,
            "chunkCount": chunk_count,
        }
    except SQLAlchemyError as exc:
        raise KnowledgeStoreUnavailableError("knowledge store unavailable") from exc


def delete_user_knowledge_document(
    db: Session, user_id: uuid.UUID, doc_id: str | uuid.UUID
) -> bool:
    try:
        parsed_doc_id = doc_id if isinstance(doc_id, uuid.UUID) else uuid.UUID(str(doc_id))
    except (ValueError, TypeError):
        return False

    try:
        doc = (
            db.query(UserKnowledgeDocument)
            .filter(
                UserKnowledgeDocument.id == parsed_doc_id,
                UserKnowledgeDocument.user_id == user_id,
            )
            .first()
        )
        if doc is None:
            return False

        db.query(UserKnowledgeChunk).filter(UserKnowledgeChunk.document_id == doc.id).delete()
        db.delete(doc)
        db.commit()
        return True
    except SQLAlchemyError as exc:
        db.rollback()
        raise KnowledgeStoreUnavailableError("knowledge store unavailable") from exc
