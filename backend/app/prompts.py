
parse_summary = "You are an assistant tasked with extracting a professional summary from a resume. " \
"Extract only the Summary / Introduction section at the beginning of the text. " \
"Return a valid JSON object with a 'summary' key containing the extracted text (or null if none found)."

parse_skills = "You are an assistant tasked with extracting a list of skills from a resume. " \
"Extract only the Skills / Technologies section. " \
"Return a valid JSON object with a 'skills' key containing an array of skill strings."

parse_experience = "You are an assistant tasked with extracting work experience from a resume. " \
"Extract only the Experience section. " \
"Return a valid JSON object with an 'experience' key containing an array of objects, " \
"each with 'company', 'title', and 'details' keys."

parse_projects = "You are an assistant tasked with extracting projects from a resume. " \
"Extract only the Projects section. " \
"Return a valid JSON object with a 'projects' key containing an array of objects, " \
"each with 'name', 'description'."

parse_prompts = [parse_summary, parse_skills, parse_experience, parse_projects]


tailor_summary = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Summary / Introduction section at the beginning of the text. Maintain a professional style, and aim to " \
"mimic the tone displayed in this resume. " \
"Analyze the job description (provided below) and suggest improvements to better align the summary with key requirements and keywords. " \
"Return a valid JSON array of suggestion objects, each with 'original', 'updated', and 'explanation'." \

tailor_skills = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Skills / Technologies section. As this section is mostly words, the list of suggestions should be to either remove " \
"irrelevant skills or add relevant skills mentioned in the job description. Only add skills that make sense - that is, don't add a non-existent skill. " \
"Analyze the job description (provided below) to identify which skills to prioritize. " \
"Return a valid JSON array of suggestion objects, each with 'original', 'updated', and 'explanation'." \

tailor_experience = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Experience section. For each experience entry, provide suggestions to more closely align the bullet points with " \
"the requirements and keywords from the job description (provided below). Do not fabricate information, only enhance existing content " \
"by emphasizing relevant achievements, technologies, or responsibilities that match the job description. " \
"Return a valid JSON array of suggestion objects, each with 'entryIdx' corresponding to which experience entry " \
"this applies to, 'bulletIdx' corresponding to which bullet point the suggestion applies to, 'original', " \
"'updated', and 'explanation'." \

tailor_projects = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Projects section. For each project, provide suggestions to more closely align the project descriptions with " \
"the requirements and keywords from the job description (provided below). Do not fabricate information, only enhance existing content " \
"by emphasizing relevant technologies, methodologies, or outcomes that match the job description. " \
"Return a valid JSON array of suggestion objects, each with 'entryIdx' corresponding to which project " \
"this applies to, 'bulletIdx' corresponding to which bullet point the suggestion applies to, 'original', " \
"'updated', and 'explanation'." \

tailor_prompts = [tailor_summary, tailor_skills, tailor_experience, tailor_projects]

tailor_schema_examples = {
    0: [
        {
            "section": "summary",
            "entryIdx": None,
            "bulletIdx": None,
            "original": "Backend developer with experience using Flask",
            "updated": "Fullstack developer specializing in backend systems and APIs",
            "explanation": "Broadens scope and emphasizes API-focused work."
        }
    ],
    1: [
        {
            "section": "skills",
            "entryIdx": "2",
            "bulletIdx": None,
            "original": "python, flask, docker",
            "updated": "python, fastapi, docker, kubernetes",
            "explanation": "Replaces Flask with FastAPI and adds Kubernetes to highlight infrastructure skills."
        }
    ],
    2: [
        {
            "section": "experience",
            "entryIdx": "0",
            "bulletIdx": "2",
            "original": "Built internal APIs.",
            "updated": "Designed and implemented scalable REST APIs using FastAPI, improving latency by 25%.",
            "explanation": "Adds technical specificity and measurable impact."
        }
    ],
    3: [
        {
            "section": "projects",
            "entryIdx": "0",
            "bulletIdx": "1",
            "original": "Designed a search engine",
            "updated": "Implemented a search engine using an inverted index and Elasticsearch for full-text search",
            "explanation": "Clarifies architecture and technologies used."
        }
    ]
}
