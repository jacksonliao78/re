# get-a-job

Full-stack app: upload a PDF resume (parsed with an LLM), browse or paste job postings, and get AI suggestions to tailor your resume—with a live PDF preview.

**Stack:** FastAPI · React + TypeScript (Vite) · PostgreSQL · LangChain (Google Generative AI) · LaTeX (`pdflatex`) for resume PDFs.

### Pages

| Route | Description |
|-------|-------------|
| **`/`** | Landing page (overview, how it works, CTA). |
| **`/resume`** | Upload a PDF, parse to structured data, preview the rendered resume, and (when signed in) manage saved context (add, view, delete) to improve tailoring quality. |
| **`/tailor`** | Scrape jobs or paste a description, fetch suggestions, apply/reject next to the PDF viewer. |

Accounts are **optional**; signing in enables a saved default resume and ignored-job filtering across sessions.

---

### Prerequisites

- **Python** 3.10+ and **Node.js** 20+
- **PostgreSQL** (local or remote)
- **Google Generative AI API key** (`GOOGLE_API_KEY`)
- **`pdflatex`** (e.g. [TeX Live](https://www.tug.org/texlive/)) for server-side PDF rendering

---

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a database and a `backend/.env` file:

```bash
createdb resumedb
```

Example `backend/.env`:

```env
DATABASE_URL=postgresql://<user>@localhost:5432/resumedb
JWT_SECRET_KEY=<long-random-string>
GOOGLE_API_KEY=<your-google-ai-key>
# Optional — must be a model your key can call (defaults in code if unset)
# GOOGLE_MODEL=gemini-2.5-flash
```

Initialize the schema and run the API:

```bash
python -m app.init_db
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** for the interactive API.

Resume-related API flow (high level):

- `POST /resume/upload` parses an uploaded resume PDF.
- `POST /resume/tailor` generates tailored suggestions from resume + job details.
- `POST /resume/knowledge` saves a context entry for the signed-in user.
- `GET /resume/knowledge` lists saved context entries for the signed-in user.
- `GET /resume/knowledge/{doc_id}` returns one saved context entry.
- `DELETE /resume/knowledge/{doc_id}` removes one saved context entry.

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: **http://localhost:5173/**. Vite proxies API paths (e.g. `/jobs`, `/resume`, `/auth`) to the backend on port **8000** (see `frontend/vite.config.ts`).

---

### Troubleshooting

| Issue | What to try |
|-------|-------------|
| `ModuleNotFoundError: No module named 'app'` | Run `uvicorn` from the `backend/` directory. |
| `GOOGLE_API_KEY` / model errors | Set the key in `backend/.env`. If you see `NOT_FOUND` for a model name, pick a supported model and set `GOOGLE_MODEL`. |
| PDF render fails | Ensure `pdflatex` is on your `PATH` and TeX can compile the template. |
| JWT / `jose` issues | Use `pip install "python-jose[cryptography]"` (not the unrelated `jose` package). |
