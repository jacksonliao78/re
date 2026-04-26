import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.rag import _chunk_text, _fallback_embedding


def test_chunk_text_splits_large_content():
    text = "A" * 1800
    chunks = _chunk_text(text, chunk_size=700, overlap=100)
    assert len(chunks) >= 3
    assert all(len(c) > 0 for c in chunks)


def test_fallback_embedding_is_normalized():
    vec = _fallback_embedding("fastapi postgres optimization")
    norm = math.sqrt(sum(v * v for v in vec))
    assert len(vec) == 64
    assert abs(norm - 1.0) < 1e-6
