from google import genai
from models import Resume
from models import Job


client = genai.Client()

def tailor_resume( resume: Resume, job: Job ):

    ###
    # to tailor the resume we will put the parsed resume through
    # a LLM in order to generate a list of suggestions based on the
    # parsed text
    ###

    ### ideally we return a list of suggetions 
    

    ...

