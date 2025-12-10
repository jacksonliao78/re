
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

prompts = [parseSummary, parseSkills, parseExperience, parseProjects]