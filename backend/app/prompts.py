
parse_heading_education = (
    "You are an assistant that extracts heading and education information from a resume. "
    "Extract ONLY:\n"
    "- Heading: full name, phone, email, overall location (city and state or country), LinkedIn URL, GitHub URL.\n"
    "- Education: each degree program, with school name, school location, degree text, start date, and end date.\n"
    "Return a single JSON object with:\n"
    "- 'heading': object with keys 'name', 'phone', 'email', 'location', 'linkedin', 'github' (use null for missing values).\n"
    "- 'education': array of objects with keys 'school', 'location', 'degree', 'start', 'end'.\n"
    "Ignore work experience, projects, skills, awards, and any other sections."
)

parse_experience_projects = (
    "You are an assistant that extracts work experience and projects from a resume. "
    "Extract ONLY:\n"
    "- Experience: each job, internship, or research role, with company, title, location, start date, end date, and bullet-point details.\n"
    "- Projects: each project, with project name, bullet-point descriptions, technologies, and an optional date range text.\n"
    "Return a single JSON object with:\n"
    "- 'experience': array of objects with keys 'company', 'title', 'location', 'start', 'end', 'details'.\n"
    "- 'projects': array of objects with keys 'name', 'description', 'tech', 'dateRange'.\n"
    "Ignore summary, education, skills, awards, and any other sections."
)

parse_summary_skills = (
    "You are an assistant that extracts programming languages and technologies from a resume. "
    "Extract ONLY:\n"
    "- Languages: programming languages (e.g. Python, Java, JavaScript, SQL, HTML, CSS, R, OCaml).\n"
    "- Technologies: frameworks, tools, libraries, and platforms (e.g. React, FastAPI, Docker, Git, PostgreSQL).\n"
    "Return a single JSON object with:\n"
    "- 'languages': array of strings (may be empty but must be present).\n"
    "- 'technologies': array of strings (may be empty but must be present).\n"
    "Ignore summary, education, experience, projects, awards, and any other content."
)

parse_prompts = [parse_heading_education, parse_experience_projects, parse_summary_skills]

# JSON schema examples for the parse prompts. These are appended to the
# instructions to force the model to emit a predictable shape.
parse_schema_examples = {
    "heading_education": {
        "heading": {
            "name": "Jane Doe",
            "phone": "123-456-7890",
            "email": "jane@example.com",
            "location": "Ithaca, NY",
            "linkedin": "https://www.linkedin.com/in/janedoe",
            "github": "https://github.com/janedoe",
        },
        "education": [
            {
                "school": "Cornell University",
                "location": "Ithaca, NY",
                "degree": "B.S. in Animal Science",
                "start": "Aug 2022",
                "end": "May 2026",
            }
        ],
    },
    "experience_projects": {
        "experience": [
            {
                "company": "American Red Cross",
                "title": "Software Engineering Intern",
                "location": "Buffalo, NY",
                "start": "June 2025",
                "end": "Aug 2025",
                "details": [
                    "Developed a REST API to archive 25,000 Jira issues",
                    "Built a Flask web app to trigger archival jobs",
                ],
            }
        ],
        "projects": [
            {
                "name": "Resume Tailorer",
                "description": [
                    "Built a full-stack app for resume parsing and tailoring"
                ],
                "tech": ["Python", "FastAPI", "React", "PostgreSQL"],
                "dateRange": "Nov 2025 -- Feb 2026",
            }
        ],
    },
    "summary_skills": {
        "languages": ["Python", "Java", "JavaScript", "SQL"],
        "technologies": ["React", "FastAPI", "Docker", "Git"],
    },
}


tailor_summary = (
    "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. "
    "Only focus on the Summary / Introduction section at the beginning of the text. Maintain a professional style, and aim to "
    "mimic the tone displayed in this resume. "
    "Analyze the job description (provided below) and suggest improvements to better align the summary with key requirements and keywords. "
    "Return a valid JSON array of suggestion objects, each with 'original', 'updated', and 'explanation'."
)

tailor_languages = (
    "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. "
    "Only focus on the Languages section (programming languages). Each suggestion should target ONE individual language. "
    "For each suggestion, provide 'entryIdx' (the array index of the language to modify, use 0 for first). "
    "The 'original' field should be the single language string currently at that index, or an empty string '' if adding a new one. "
    "The 'updated' field should be the new single language string, or an empty string '' if removing. "
    "Three types: (1) Replace: original=existing, updated=new, entryIdx=current index. "
    "(2) Remove: original=existing, updated='', entryIdx=current index. "
    "(3) Add: original='', updated=new language, entryIdx can be any value (will be appended). "
    "Only suggest languages the person actually knows based on their resume context. "
    "Analyze the job description (provided below) to identify which languages to add, replace, or remove. "
    "Return a valid JSON array of suggestion objects, each with 'entryIdx', 'original', 'updated', and 'explanation'."
)

tailor_technologies = (
    "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. "
    "Only focus on the Technologies section (frameworks, tools, libraries, platforms). Each suggestion should target ONE individual technology. "
    "For each suggestion, provide 'entryIdx' (the array index of the technology to modify, use 0 for first). "
    "The 'original' field should be the single technology string currently at that index, or an empty string '' if adding a new one. "
    "The 'updated' field should be the new single technology string, or an empty string '' if removing. "
    "Three types: (1) Replace: original=existing, updated=new, entryIdx=current index. "
    "(2) Remove: original=existing, updated='', entryIdx=current index. "
    "(3) Add: original='', updated=new technology, entryIdx can be any value (will be appended). "
    "Only suggest technologies the person actually knows based on their resume context. "
    "Analyze the job description (provided below) to identify which technologies to add, replace, or remove. "
    "Return a valid JSON array of suggestion objects, each with 'entryIdx', 'original', 'updated', and 'explanation'."
)

tailor_technologies = (
    "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. "
    "Only focus on the Technologies section (frameworks, tools, libraries, platforms). Each suggestion should target ONE individual technology. "
    "For each suggestion, provide 'entryIdx' (the array index of the technology to modify, use 0 for first). "
    "The 'original' field should be the single technology string currently at that index, or an empty string '' if adding a new one. "
    "The 'updated' field should be the new single technology string, or an empty string '' if removing. "
    "Three types: (1) Replace: original=existing, updated=new, entryIdx=current index. "
    "(2) Remove: original=existing, updated='', entryIdx=current index. "
    "(3) Add: original='', updated=new technology, entryIdx can be any value (will be appended). "
    "Only suggest technologies the person actually knows based on their resume context. "
    "Analyze the job description (provided below) to identify which technologies to add, replace, or remove. "
    "Return a valid JSON array of suggestion objects, each with 'entryIdx', 'original', 'updated', and 'explanation'."
)

tailor_experience = (
    "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. "
    "Only focus on the Experience section. For each experience entry, provide suggestions to more closely align the bullet points with "
    "the requirements and keywords from the job description (provided below). Do not fabricate information, only enhance existing content "
    "by emphasizing relevant achievements, technologies, or responsibilities that match the job description. "
    "Return a valid JSON array of suggestion objects, each with 'entryIdx' corresponding to which experience entry "
    "this applies to, 'bulletIdx' corresponding to which bullet point the suggestion applies to, 'original', "
    "'updated', and 'explanation'."
)

tailor_prompts = [tailor_summary, tailor_languages, tailor_technologies, tailor_experience]

# JSON schema examples for the tailor prompts. These are appended to the
# instructions to force the model to emit a predictable shape.
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
            "section": "languages",
            "entryIdx": "1",
            "bulletIdx": None,
            "original": "R",
            "updated": "",
            "explanation": "Removes R since it is not relevant to this role."
        },
        {
            "section": "languages",
            "entryIdx": "5",
            "bulletIdx": None,
            "original": "",
            "updated": "Go",
            "explanation": "Adds Go as a language since the job description mentions it."
        }
    ],
    2: [
        {
            "section": "technologies",
            "entryIdx": "2",
            "bulletIdx": None,
            "original": "Docker",
            "updated": "Kubernetes",
            "explanation": "Replaces Docker with Kubernetes to highlight container orchestration skills."
        },
        {
            "section": "technologies",
            "entryIdx": "5",
            "bulletIdx": None,
            "original": "",
            "updated": "AWS",
            "explanation": "Adds AWS to highlight cloud experience mentioned in the job description."
        }
    ],
    3: [
        {
            "section": "experience",
            "entryIdx": "0",
            "bulletIdx": "2",
            "original": "Built internal APIs.",
            "updated": "Designed and implemented scalable REST APIs using FastAPI, improving latency by 25%.",
            "explanation": "Adds technical specificity and measurable impact."
        }
    ],
    4: [
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
