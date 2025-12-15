
parseSummary = "You are an assistant tasked with extracting a professional summary from a resume. " \
"Extract only the Summary / Introduction section at the beginning of the text. " \
"Return a valid JSON object with a 'summary' key containing the extracted text (or null if none found)."

parseSkills = "You are an assistant tasked with extracting a list of skills from a resume. " \
"Extract only the Skills / Technologies section. " \
"Return a valid JSON object with a 'skills' key containing an array of skill strings."

parseExperience = "You are an assistant tasked with extracting work experience from a resume. " \
"Extract only the Experience section. " \
"Return a valid JSON object with an 'experience' key containing an array of objects, " \
"each with 'company', 'title', and 'details' keys."

parseProjects = "You are an assistant tasked with extracting projects from a resume. " \
"Extract only the Projects section. " \
"Return a valid JSON object with a 'projects' key containing an array of objects, " \
"each with 'name', 'description'."

parsePrompts = [parseSummary, parseSkills, parseExperience, parseProjects]


tailorSummary = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Summary / Introduction section at the beginning of the text. Maintain a professional style, and aim to " \
"mimic the tone displayed in this resume." \
"Return a valid JSON object with a containing an array of suggestions." 

tailorSkills = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Skills / Technolgies section. As this section is mostly words, the list of suggestions should be to either remove " \
"or add a skill. Only add skills that make sense - that is, don't add a non-existant skill. " \
"Return a valid JSON object with a containing an array of suggestions." 

tailorExperience = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Experience section. For each experience, provide a list of suggestions to more closely align the experience with" \
"what the job description desires. Do not fabricate information, only enhance it." \
"Return a valid JSON object with a containing an array of suggestions." 

tailorProjects = "You are an assistant tasked with providing a list of suggestions for a resume based on a job description. " \
"Only focus on the Projects section. For each project, provide a list of suggestions to more closely align the experience with" \
"what the job description desires. Do not fabricate information, only enhance it." \
"Return a valid JSON object with a containing an array of suggestions." 

tailorPrompts = [tailorSummary, tailorSkills, tailorExperience, tailorProjects]