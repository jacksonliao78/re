from app.models import Resume, Job, Suggestion
from app.prompts import tailor_prompts, tailor_schema_examples
from app.llm import get_model, parse_json
from app.rag import retrieve_relevant_chunks, KnowledgeStoreUnavailableError
import json
import uuid
from sqlalchemy.orm import Session


def _format_evidence(chunks: list[dict]) -> str:
    if not chunks:
        return ""
    lines: list[str] = ["\nRetrieved user evidence (RAG):"]
    for c in chunks:
        chunk_id = c.get("chunkId", "")
        score = c.get("score", 0)
        text = str(c.get("text", "")).strip()
        if text:
            lines.append(f"- [chunkId={chunk_id} score={score}] {text}")
    return "\n".join(lines)


def tailor_resume( resume: Resume, job: Job ) -> list[Suggestion]:
    return _tailor_resume_core(resume=resume, job=job, evidence_chunks=None)


def _tailor_resume_core(
    resume: Resume,
    job: Job,
    evidence_chunks: list[dict] | None = None,
) -> list[Suggestion]:
    suggestions: list[Suggestion] = []
    job_description = (job.description or "").strip()

    model = get_model()

    keys = [ "languages", "technologies", "experience" ]

    parsed_outputs = {}

    for i in range( len(tailor_prompts) ):

        if( getattr( resume, keys[i] ) is None ): continue

        output_instructions = (
            "IMPORTANT: Do NOT force yourself to create suggestions by fabricating information. It is ok to return an empty list. Reply with valid JSON only and nothing else. Do NOT include any explanatory text, markdown, or backticks. The JSON must match the schema example below exactly (use the same keys):\n"
            + json.dumps(tailor_schema_examples[i], indent=2)
        )
        
        resume_instruction = "Here is the parsed resume you can use to contextualize your edits: \n" + resume.to_string()
        grounding_instruction = ""
        if evidence_chunks:
            grounding_instruction = (
                "\nIMPORTANT grounding rules:\n"
                "- Only propose edits grounded in either the parsed resume or retrieved evidence.\n"
                "- If you cannot ground a claim, return no suggestion.\n"
                + _format_evidence(evidence_chunks)
            )

        system_prompt = tailor_prompts[i] + output_instructions + resume_instruction + grounding_instruction

        message = [("system", system_prompt), ("human", job_description)]

        res = model.invoke( message )

        raw = getattr( res, "text", str(res) )

        parsed = parse_json(raw)

        if parsed is None:
            parsed_outputs[ keys[i] ] = None
        else:
            parsed_outputs[ keys[i] ] = parsed
            #print(f"Parsed {keys[i]}:")
            #print(json.dumps(parsed, indent=2))

        section = keys[i]
        if parsed_outputs[ keys[i] ] is not None:
            for suggestion in parsed_outputs[ keys[i] ]:
                # Convert string indices to integers if present (LLM may return strings)
                entry_idx = suggestion.get("entryIdx")
                entry_idx_int = None
                if entry_idx is not None and entry_idx != "":
                    try:
                        entry_idx_int = int(entry_idx)
                    except (ValueError, TypeError):
                        entry_idx_int = None
                    
                bullet_idx = suggestion.get("bulletIdx")
                bullet_idx_int = None
                if bullet_idx is not None and bullet_idx != "":
                    try:
                        bullet_idx_int = int(bullet_idx)
                    except (ValueError, TypeError):
                        bullet_idx_int = None
                
                s = Suggestion(
                    section=section,
                    entryIdx=entry_idx_int,
                    bulletIdx=bullet_idx_int,
                    original=suggestion["original"],
                    updated=suggestion["updated"],
                    explanation=suggestion["explanation"]
                )

                suggestions.append( s )

    return suggestions


def tailor_resume_with_rag(
    resume: Resume,
    job: Job,
    db: Session,
    user_id: uuid.UUID | None,
) -> list[Suggestion]:
    """
    RAG-first tailoring for authenticated users with stored knowledge.
    Falls back to legacy tailoring when no user knowledge is available.
    """
    if user_id is None:
        return tailor_resume(resume, job)

    query = (
        f"Job title: {job.title}\n"
        f"Company: {job.company or ''}\n"
        f"Description: {job.description or ''}\n"
        "Find relevant resume evidence for languages, technologies, and experience bullets."
    )
    try:
        chunks = retrieve_relevant_chunks(db=db, user_id=user_id, query_text=query, top_k=10)
    except KnowledgeStoreUnavailableError:
        return tailor_resume(resume, job)
    if not chunks:
        return tailor_resume(resume, job)
    return _tailor_resume_core(resume=resume, job=job, evidence_chunks=chunks)


