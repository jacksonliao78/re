from app.models import Resume, Job, Suggestion
from app.prompts import tailor_prompts, tailor_schema_examples
from app.llm import get_model, parse_json
import json


def tailor_resume( resume: Resume, job: Job ) -> list[Suggestion]:
    
    suggestions: list[Suggestion] = []

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

        system_prompt = tailor_prompts[i] + output_instructions + resume_instruction

        message = [ ("system", system_prompt), ("human", job.description ) ]

        res = model.invoke( message )

        raw = getattr( res, "text", str(res) )

        print(raw)

        parsed = parse_json(raw)

        if parsed is None:
            print("failed to parse JSON")
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


