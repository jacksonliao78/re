import os
import re
import json
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

PLACEHOLDER_STRINGS = {
    "not specified", "n/a", "na", "none", "unknown", "null", "unspecified",
    "not available", "not provided", "not listed", "not mentioned",
}


def get_model():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set.\n"
            "Set it locally with: export GOOGLE_API_KEY=your_key\n"
            "Or create a .env file with: GOOGLE_API_KEY=your_key"
        )

    model_name = os.environ.get("GOOGLE_MODEL", "gemini-3.1-flash-lite-preview")
    #TODO allow any model from any provider

    return ChatGoogleGenerativeAI(
        model=model_name,
        retries=2,
        api_key=api_key,
        temperature=0,
        model_kwargs={"response_mime_type": "application/json"},
    )


def get_embeddings_model():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    model_name = os.environ.get("GOOGLE_EMBEDDING_MODEL", "models/text-embedding-004")
    try:
        return GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=api_key)
    except Exception:
        return None



#just parse json if possible, ignoring markdown ticks and such
def parse_json(raw: str) -> Any | None:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    try:
        return json.loads(raw)
    except Exception:
        m = re.search(r"(\{.*\}|\[.*\])", raw, re.S)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                return None
    return None



#output cleaning if necessary 

def _is_placeholder(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDER_STRINGS

def sanitize_nulls(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: sanitize_nulls(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_nulls(item) for item in obj]
    if isinstance(obj, str) and _is_placeholder(obj):
        return None
    return obj
