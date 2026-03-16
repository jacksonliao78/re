import os
from pathlib import Path
import subprocess
import tempfile
from typing import Dict

from app.models import Resume, EducationEntry, Experience, Project


TEMPLATE_PATH = Path(__file__).parent / "templates" / "jakes_resume.tex"


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
    "\\": r"\textbackslash{}",
}


def escape_latex(text: str | None) -> str:
    if not text:
        return ""
    result: list[str] = []
    for ch in text:
        if ch in LATEX_SPECIAL_CHARS:
            result.append(LATEX_SPECIAL_CHARS[ch])
        else:
            result.append(ch)
    return "".join(result)


def _render_heading(resume: Resume) -> str:
    if not resume.heading:
        return ""

    name = escape_latex(resume.heading.name or "")
    bits: list[str] = []

    if resume.heading.phone:
        bits.append(escape_latex(resume.heading.phone))
    if resume.heading.email:
        bits.append(
            r"\href{mailto:%s}{\underline{%s}}"
            % (
                escape_latex(resume.heading.email),
                escape_latex(resume.heading.email),
            )
        )
    if resume.heading.linkedin:
        bits.append(
            r"\href{%s}{\underline{%s}}"
            % (
                escape_latex(resume.heading.linkedin),
                escape_latex(resume.heading.linkedin),
            )
        )
    if resume.heading.github:
        bits.append(
            r"\href{%s}{\underline{%s}}"
            % (
                escape_latex(resume.heading.github),
                escape_latex(resume.heading.github),
            )
        )

    contact = " $|$ ".join(bits) if bits else ""
    return (
        r"\begin{center}" + "\n"
        r"    \textbf{\Huge \scshape %s} \\ \vspace{1pt}" % name
        + ("\n    \\small %s" % contact if contact else "")
        + "\n\\end{center}\n"
    )


def _render_education_entry(e: EducationEntry) -> str:
    school = escape_latex(e.school or "")
    location = escape_latex(e.location or "")
    degree = escape_latex(e.degree or "")
    date_range = escape_latex(
        " - ".join([d for d in [e.start or "", e.end or ""] if d])
    )
    return (
        r"\resumeSubheading{%s}{%s}{%s}{%s}"
        % (school, location, degree, date_range)
    )


def _render_education(resume: Resume) -> str:
    if not resume.education:
        return ""
    lines = [r"\section{Education}", r"\resumeSubHeadingListStart"]
    for edu in resume.education:
        lines.append(_render_education_entry(edu))
    lines.append(r"\resumeSubHeadingListEnd")
    return "\n".join(lines) + "\n"


def _render_experience_entry(e: Experience) -> str:
    title = escape_latex(e.title or "")
    company = escape_latex(e.company or "")
    location = escape_latex(e.location or "")
    date_range = escape_latex(
        " - ".join([d for d in [e.start or "", e.end or ""] if d])
    )
    header = r"\resumeSubheading{%s}{%s}{%s}{%s}" % (
        title or "",
        date_range,
        company or "",
        location or "",
    )
    bullets: list[str] = []
    if e.details:
        bullets.append(r"\resumeItemListStart")
        for detail in e.details:
            bullets.append(r"\resumeItem{%s}" % escape_latex(detail))
        bullets.append(r"\resumeItemListEnd")
    return "\n".join([header] + bullets)


def _render_experience(resume: Resume) -> str:
    if not resume.experience:
        return ""
    lines = [r"\section{Experience}", r"\resumeSubHeadingListStart"]
    for exp in resume.experience:
        lines.append(_render_experience_entry(exp))
    lines.append(r"\resumeSubHeadingListEnd")
    return "\n".join(lines) + "\n"


def _render_project_entry(p: Project) -> str:
    name = escape_latex(p.name or "")
    tech_line = ""
    if p.tech:
        tech_line = r"\textbf{%s}" % escape_latex(", ".join(p.tech))
    heading_left = name
    if tech_line:
        heading_left = r"\textbf{%s} $|$ \emph{%s}" % (name, tech_line)
    date_range = escape_latex(p.dateRange or "")
    header = r"\resumeProjectHeading{%s}{%s}" % (heading_left, date_range)
    bullets: list[str] = []
    if p.description:
        bullets.append(r"\resumeItemListStart")
        for desc in p.description:
            bullets.append(r"\resumeItem{%s}" % escape_latex(desc))
        bullets.append(r"\resumeItemListEnd")
    return "\n".join([header] + bullets)


def _render_projects(resume: Resume) -> str:
    if not resume.projects:
        return ""
    lines = [r"\section{Projects}", r"\resumeSubHeadingListStart"]
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


def resume_to_latex_sections(resume: Resume) -> Dict[str, str]:
    return {
        "HEADING": _render_heading(resume),
        "EDUCATION": _render_education(resume),
        "EXPERIENCE": _render_experience(resume),
        "PROJECTS": _render_projects(resume),
        "SKILLS": _render_skills(resume),
    }


def build_latex_document(resume: Resume) -> str:
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    sections = resume_to_latex_sections(resume)
    for key, value in sections.items():
        template_text = template_text.replace(f"{{{{{key}}}}}", value)
    return template_text


def render_resume_pdf(resume: Resume) -> bytes:
    """
    Build a LaTeX document for the given resume and compile it to PDF.
    Returns the PDF bytes. Raises RuntimeError on failure.
    """
    latex_source = build_latex_document(resume)
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = Path(tmpdir) / "resume.tex"
        tex_path.write_text(latex_source, encoding="utf-8")

        # Run pdflatex; on failure, read the .log file for diagnostics.
        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_path.name],
                cwd=tmpdir,
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to run pdflatex: {exc}") from exc

        log_path = Path(tmpdir) / "resume.log"
        log_snippet = ""
        if log_path.exists():
            try:
                log_text = log_path.read_text(encoding="utf-8", errors="ignore")
                log_snippet = "\n".join(log_text.splitlines()[-40:])
            except Exception:
                log_snippet = ""

        if result.returncode != 0:
            raise RuntimeError(
                f"pdflatex failed with exit code {result.returncode}. "
                f"Last log lines:\n{log_snippet}"
            )

        pdf_path = Path(tmpdir) / "resume.pdf"
        if not pdf_path.exists():
            raise RuntimeError("LaTeX compilation did not produce resume.pdf")

        return pdf_path.read_bytes()

