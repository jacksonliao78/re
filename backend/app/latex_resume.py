import os
import subprocess
import tempfile

from app.models import Resume

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "jakes_resume.tex")

LATEX_SPECIAL_CHARS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(text: str) -> str:
    if not text:
        return ""
    result: list[str] = []
    for ch in text:
        if ch == "\\":
            result.append(r"\textbackslash{}")
        elif ch in LATEX_SPECIAL_CHARS:
            result.append(LATEX_SPECIAL_CHARS[ch])
        else:
            result.append(ch)
    return "".join(result)


def _render_heading(resume: Resume) -> str:
    h = resume.heading
    if not h:
        return ""
    lines: list[str] = []
    name = escape_latex(h.name or "Your Name")
    lines.append(r"\begin{center}")
    lines.append(r"  \textbf{\Huge \scshape %s} \\ \vspace{1pt}" % name)

    contact_parts: list[str] = []
    if h.phone:
        contact_parts.append(escape_latex(h.phone))
    if h.email:
        safe_email = escape_latex(h.email)
        contact_parts.append(r"\href{mailto:%s}{\underline{%s}}" % (h.email, safe_email))
    if h.linkedin:
        safe_li = escape_latex(h.linkedin)
        contact_parts.append(r"\href{%s}{\underline{%s}}" % (h.linkedin, safe_li))
    if h.github:
        safe_gh = escape_latex(h.github)
        contact_parts.append(r"\href{%s}{\underline{%s}}" % (h.github, safe_gh))
    if h.location:
        contact_parts.append(escape_latex(h.location))

    if contact_parts:
        lines.append(r"  \small " + r" $|$ ".join(contact_parts))

    lines.append(r"\end{center}")
    return "\n".join(lines) + "\n"


def _render_education_entry(edu) -> str:
    school = escape_latex(edu.school or "")
    location = escape_latex(edu.location or "")
    degree = escape_latex(edu.degree or "")
    dates = ""
    if edu.start or edu.end:
        start = escape_latex(edu.start or "")
        end = escape_latex(edu.end or "")
        dates = f"{start} -- {end}" if start and end else start or end
    return r"  \resumeSubheading{%s}{%s}{%s}{%s}" % (school, location, degree, dates)


def _render_education(resume: Resume) -> str:
    if not resume.education:
        return ""
    lines: list[str] = []
    lines.append(r"\section{Education}")
    lines.append(r"\resumeSubHeadingListStart")
    for edu in resume.education:
        lines.append(_render_education_entry(edu))
    lines.append(r"\resumeSubHeadingListEnd")
    return "\n".join(lines) + "\n"


def _render_experience_entry(exp) -> str:
    lines: list[str] = []
    company = escape_latex(exp.company or "")
    title = escape_latex(exp.title or "")
    location = escape_latex(exp.location or "")
    dates = ""
    if exp.start or exp.end:
        start = escape_latex(exp.start or "")
        end = escape_latex(exp.end or "")
        dates = f"{start} -- {end}" if start and end else start or end
    lines.append(r"  \resumeSubheading{%s}{%s}{%s}{%s}" % (company, dates, title, location))
    if exp.details:
        lines.append(r"    \resumeItemListStart")
        for detail in exp.details:
            lines.append(r"      \resumeItem{%s}" % escape_latex(detail))
        lines.append(r"    \resumeItemListEnd")
    return "\n".join(lines)


def _render_experience(resume: Resume) -> str:
    if not resume.experience:
        return ""
    lines: list[str] = []
    lines.append(r"\section{Experience}")
    lines.append(r"\resumeSubHeadingListStart")
    for exp in resume.experience:
        lines.append(_render_experience_entry(exp))
    lines.append(r"\resumeSubHeadingListEnd")
    return "\n".join(lines) + "\n"


def _render_project_entry(proj) -> str:
    lines: list[str] = []
    name = escape_latex(proj.name or "")
    tech_str = ""
    if proj.tech:
        tech_str = ", ".join(escape_latex(t) for t in proj.tech)
        tech_str = r" $|$ \emph{%s}" % tech_str
    date_range = escape_latex(proj.dateRange or "")
    lines.append(r"  \resumeProjectHeading{\textbf{%s}%s}{%s}" % (name, tech_str, date_range))
    if proj.description:
        lines.append(r"    \resumeItemListStart")
        for desc in proj.description:
            lines.append(r"      \resumeItem{%s}" % escape_latex(desc))
        lines.append(r"    \resumeItemListEnd")
    return "\n".join(lines)


def _render_projects(resume: Resume) -> str:
    if not resume.projects:
        return ""
    lines: list[str] = []
    lines.append(r"\section{Projects}")
    lines.append(r"\resumeSubHeadingListStart")
    for proj in resume.projects:
        lines.append(_render_project_entry(proj))
    lines.append(r"\resumeSubHeadingListEnd")
    return "\n".join(lines) + "\n"


def _render_skills(resume: Resume) -> str:
    if not resume.languages and not resume.technologies:
        return ""
    lines: list[str] = []
    lines.append(r"\section{Technical Skills}")
    lines.append(r"\begin{itemize}[leftmargin=0.15in, label={}]")
    lines.append(r"  \small{\item{")
    if resume.languages:
        lang_line = ", ".join(escape_latex(s) for s in resume.languages)
        lines.append(r"   \textbf{Languages}{: %s} \\" % lang_line)
    if resume.technologies:
        tech_line = ", ".join(escape_latex(s) for s in resume.technologies)
        lines.append(r"   \textbf{Technologies}{: %s}" % tech_line)
    lines.append(r"  }}")
    lines.append(r"\end{itemize}")
    return "\n".join(lines) + "\n"


def resume_to_latex_sections(resume: Resume) -> dict[str, str]:
    return {
        "HEADING": _render_heading(resume),
        "EDUCATION": _render_education(resume),
        "EXPERIENCE": _render_experience(resume),
        "PROJECTS": _render_projects(resume),
        "SKILLS": _render_skills(resume),
    }


def build_latex_document(resume: Resume) -> str:
    with open(TEMPLATE_PATH, "r") as f:
        template = f.read()
    sections = resume_to_latex_sections(resume)
    for key, value in sections.items():
        template = template.replace("{{%s}}" % key, value)
    return template


def render_resume_pdf(resume: Resume) -> bytes:
    latex_source = build_latex_document(resume)

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        with open(tex_path, "w") as f:
            f.write(latex_source)

        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "resume.tex"],
            cwd=tmpdir,
            capture_output=True,
            timeout=30,
        )

        pdf_path = os.path.join(tmpdir, "resume.pdf")
        if result.returncode != 0 or not os.path.exists(pdf_path):
            log_path = os.path.join(tmpdir, "resume.log")
            log_snippet = ""
            if os.path.exists(log_path):
                with open(log_path, "r", errors="replace") as lf:
                    log_lines = lf.readlines()
                    log_snippet = "".join(log_lines[-40:])
            raise RuntimeError(
                f"pdflatex failed with exit code {result.returncode}. "
                f"Last log lines:\n{log_snippet}"
            )

        with open(pdf_path, "rb") as f:
            return f.read()
