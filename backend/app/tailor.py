from backend.app.models import Resume, Job, Suggestion
from backend.app.prompts import tailor_prompts, tailor_schema_examples
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
import re



try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def tailor_resume( resume: Resume, job: Job ) -> list[Suggestion]:
    
    suggestions: list[Suggestion] = []
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set.\n"
            "Set it locally with: export GOOGLE_API_KEY=your_key\n"
            "Or create a .env file with: GOOGLE_API_KEY=your_key"
        )

    # temp 0 to encourage deterministic output.
    model = ChatGoogleGenerativeAI( model="gemini-2.5-flash", retries=2, api_key=api_key, temperature=0 ) 

    keys = [ "summary", "skills", "experience", "projects" ]

    parsed_outputs = {}

    #first we need to give it the resume



    for i in range( len(tailor_prompts) ):

        #skip if that thing doesn't exist
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

        # try to parse JSON directly, or substring if possible 
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            # first JSON 
            m = re.search( r"(\{.*\}|\[.*\])", raw, re.S ) #regex
            if m:
                try:
                    parsed = json.loads(m.group(1))
                except Exception:
                    parsed = None

        if parsed is None:
            print("failed to parse JSON")
            parsed_outputs[ keys[i] ] = None
        else:
            parsed_outputs[ keys[i] ] = parsed
            #print(f"Parsed {keys[i]}:")
            #print(json.dumps(parsed, indent=2))

        section = keys[i]
        for suggestion in parsed_outputs[ keys[i] ]:
            s = Suggestion()
            s.section = section
            s.entryIdx = suggestion["entryIdx"] if suggestion["entryIdx"] else None
            s.bulletIdx = suggestion["bulletIdx"] if suggestion["bulletIdx"] else None 
            s.original = suggestion["original"]
            s.updated = suggestion["updated"]
            s.explanation = suggestion["explanation"]

            suggestions.append( s )

    return suggestions


