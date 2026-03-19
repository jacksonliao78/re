## get-a-job

A full-stack app that parses PDF resumes, scrapes job postings, and uses an LLM to generate tailored resume suggestions.

### Pages

- **Resume** (`/`) — Upload a PDF resume and preview the rendered output.
- **Tailor** (`/tailor`) — Browse scraped jobs or paste a description, then generate and apply AI suggestions side-by-side with a live PDF preview.

Accounts are optional. Logging in unlocks a saved default resume and ignored-job filtering across sessions.

---

### Prerequisites

- **Python** 3.10+ and **Node.js** 20+
- **PostgreSQL** running locally
- A **Google Generative AI API key**

---

### Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create the database and configure environment variables:

```bash
createdb resumedb
cp .env.example .env
```

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://<your-db-user>@localhost:5432/resumedb
JWT_SECRET_KEY=replace-with-a-long-random-string
GOOGLE_API_KEY=your-google-generative-ai-key
```

Initialize tables and start the server:

```bash
python -m app.init_db
uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs`.

---

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173/`. The Vite dev server proxies `/jobs`, `/resume`, and `/auth` to the backend on port 8000.

---

### Common issues

- **`ModuleNotFoundError: No module named 'app'`** — Run `uvicorn` from inside `backend/`.
- **JWT `jose.py` syntax error** — Wrong package installed. Run `pip uninstall -y jose && pip install "python-jose[cryptography]"`.
- **GOOGLE_API_KEY error** — Check that the key is set in `backend/.env`.
