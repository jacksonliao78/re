
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
"Only focus on the Skills / Technologies section. Each suggestion should target ONE individual skill. " \
"For each suggestion, provide 'entryIdx' (the array index of the skill to modify, use 0 for first skill). " \
"The 'original' field should be the single skill string currently at that index, or an empty string '' if adding a new skill. " \
"The 'updated' field should be the new single skill string, or an empty string '' if removing the skill. " \
"Three types of suggestions: (1) Replace: original=existing skill, updated=new skill, entryIdx=skill's current index. " \
"(2) Remove: original=existing skill, updated='', entryIdx=skill's current index. " \
"(3) Add: original='', updated=new skill to add, entryIdx can be any value (will be appended). " \
"Only suggest skills that make sense - don't add non-existent skills. " \
"Analyze the job description (provided below) to identify which skills to add, replace, or remove. " \
"Return a valid JSON array of suggestion objects, each with 'entryIdx', 'original', 'updated', and 'explanation'." \

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
            "entryIdx": "1",
            "bulletIdx": None,
            "original": "flask",
            "updated": "",
            "explanation": "Replaces flask since it is completely irrelevant."
        },
        {
            "section": "skills",
            "entryIdx": "2",
            "bulletIdx": None,
            "original": "docker",
            "updated": "kubernetes",
            "explanation": "Replaces Docker with Kubernetes to highlight container orchestration skills."
        },
        {
            "section": "skills",
            "entryIdx": "5",
            "bulletIdx": None,
            "original": "",
            "updated": "kubernetes",
            "explanation": "Adds Kubernetes as a new skill to highlight container orchestration experience."
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
