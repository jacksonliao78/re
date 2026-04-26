import asyncio
import os
import sys
import uuid
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import dependencies
from app.api import resume as resume_api
from app.models import Job, KnowledgeDocumentIn, Resume
from app.rag import KnowledgeStoreUnavailableError
from app.tailor import tailor_resume_with_rag


def test_required_auth_malformed_sub_returns_401(monkeypatch):
    monkeypatch.setattr(
        dependencies,
        "decode_access_token",
        lambda _token: {"sub": "not-a-uuid"},
    )
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="token")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(dependencies.get_current_user(credentials=credentials, db=object()))

    assert exc_info.value.status_code == 401


def test_job_accepts_job_description_alias():
    job = Job(
        id="1",
        title="Backend Engineer",
        url="https://example.com/jobs/1",
        jobDescription="Build APIs",
    )
    assert job.description == "Build APIs"


def test_tailor_with_rag_falls_back_when_knowledge_unavailable(monkeypatch):
    fallback = [{"section": "experience"}]
    monkeypatch.setattr(
        "app.tailor.retrieve_relevant_chunks",
        lambda **_kwargs: (_ for _ in ()).throw(
            KnowledgeStoreUnavailableError("knowledge store unavailable")
        ),
    )
    monkeypatch.setattr("app.tailor.tailor_resume", lambda _resume, _job: fallback)

    out = tailor_resume_with_rag(
        resume=Resume(),
        job=Job(id="1", title="x", url="https://example.com", description="desc"),
        db=object(),
        user_id=uuid.uuid4(),
    )
    assert out == fallback


def test_create_knowledge_returns_503_when_store_unavailable(monkeypatch):
    monkeypatch.setattr(
        resume_api,
        "ingest_user_knowledge",
        lambda **_kwargs: (_ for _ in ()).throw(
            KnowledgeStoreUnavailableError("knowledge store unavailable")
        ),
    )
    body = KnowledgeDocumentIn(title="t", content="c", sourceType="note")
    current_user = SimpleNamespace(id=uuid.uuid4())

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            resume_api.create_knowledge_doc(body=body, db=object(), current_user=current_user)
        )

    assert exc_info.value.status_code == 503
