from models import Resume
from models import Job
from models import Suggestion
from prompts import tailorPrompts
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI



try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def tailor_resume( resume: Resume, job: Job ) -> list[Suggestion]:

    ###
    # to tailor the resume we will put the parsed resume through
    # a LLM in order to generate a list of suggestions based on the
    # parsed text
    ###

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

    schema_examples = {
            0: {"summary": ["Consider including 'fullstack engineer' instead of just backend."] },
            1: {"skills": ["Replace Flask with FastAPI."]},
            2: {"experience": [["Use a more active word such as 'engaged'.", "Try to quantify this action."], ]},
            3: {"projects": [["",""]]}
        }

    for i in range( len(tailorPrompts) ):

        #skip if that thing doesn't exist
        if( getattr( resume, keys[i] ) is None ): continue

        output_instructions = (
            "IMPORTANT: Reply with valid JSON only and nothing else. Do NOT include any explanatory text, markdown, or backticks. The JSON must match the schema example below exactly (use the same keys):\n"
            + json.dumps(schema_examples[i], indent=2)
        )
        
        

        ...




    # we first need to give the llm a copy of the resume to read over and memorize, then we can prompt 

    ### ideally we return a list of suggetions 


    

    ...

