## get-a-job – Local Setup

This repo is a small full‑stack app that:

- Uploads and parses a PDF resume
- Scrapes or pastes job descriptions
- Uses an LLM to generate tailored resume suggestions
- (Optionally) lets users register / log in with a PostgreSQL backend

Below is how to run everything locally.

---

## 1. Prerequisites

- **Git**
- **Python**: 3.11.x or 3.10.x recommended  
  - Python 3.14 works but some dependencies (Pydantic V1 / LangChain) print compatibility warnings.
- **Node.js + npm**: recent LTS (e.g. 20.x)
- **PostgreSQL**: running locally (e.g. via Homebrew on macOS)
- A **Google Generative AI API key** (for resume parsing / tailoring)

---

## 2. Clone the repo

```bash
git clone <this-repo-url>
cd re
```

---

## 3. Backend setup (FastAPI + PostgreSQL)

From the project root:

```bash
cd backend
python -m venv venv           # create virtualenv (once)
source venv/bin/activate      # macOS / Linux

pip install -r requirements.txt
```

### 3.1 PostgreSQL database

1. Make sure postgres is running (on macOS with Homebrew, for example):

   ```bash
   brew services start postgresql@16   # or your installed version
   ```

2. Create a database (name is up to you, example: `resumedb`):

   ```bash
   createdb resumedb
   ```

3. Create a `.env` file in `backend/` based on the example:

   ```bash
   cp .env.example .env
   ```

   Then edit `backend/.env` and set at least:

   ```env
   DATABASE_URL=postgresql://<your-db-user>@localhost:5432/resumedb
   JWT_SECRET_KEY=replace-with-a-long-random-string
   GOOGLE_API_KEY=your-google-generative-ai-key
   ```

   - `<your-db-user>` is whatever user can connect locally (often your macOS username).

4. Initialize tables (run again after pulling changes that add new tables/columns):

   ```bash
   cd backend
   source venv/bin/activate
   python -m app.init_db
   ```

   You should see log output indicating tables were created (e.g. `users`, `ignored_jobs`).

For more detail / troubleshooting, see `backend/SETUP_DATABASE.md`.

### 3.2 Run the backend

From `backend/` with the venv activated:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- `http://localhost:8000/` – basic health endpoint
- `http://localhost:8000/docs` – interactive Swagger docs

Key routes:

- `POST /resume/upload` – upload a PDF (multipart/form-data) and get parsed resume JSON
- `POST /resume/tailor` – send `{ resume, job }` JSON, receive an array of suggestions
- `POST /jobs/search` – scrape jobs given a search query
- `POST /auth/register`, `/auth/login`, `GET /auth/me` – auth (JWT)
- `GET /auth/me/default-resume`, `PUT /auth/me/default-resume` – stored default resume
- `GET /auth/me/ignored-jobs`, `POST /auth/me/ignored-jobs` – ignored job IDs (filtered from scrape when logged in)

---

## 4. Frontend setup (Vite + React)

Open a new terminal window/tab, from the project root:

```bash
cd frontend
npm install          # once
npm run dev
```

By default, the app will be available at:

- `http://localhost:5173/`

The Vite dev server is configured to proxy API calls to the backend:

- `/jobs`  → `http://localhost:8000/jobs`
- `/resume` → `http://localhost:8000/resume`
- `/auth`  → `http://localhost:8000/auth`

Make sure the backend is running first so the proxy can connect.

---

## 5. Using the app

You must **log in or register** to use the app. After that:

1. **Upload a resume**
   - At the top, drag & drop a PDF or click to browse.
   - After upload, the parsed resume appears in the read‑only editor on the left.
   - **Save as default resume**: When logged in, you can click **“Save as default resume”** to store this as your baseline. It will be loaded when you next log in and used when you **rechoose** a job (resetting the working copy to this default).

2. **Select or paste a job**
   - Use **job selector + “Scrape jobs”** to fetch job postings. When logged in, jobs you’ve **ignored** or **completed** are filtered out automatically (by stable job id).
   - Or **paste a job description** and click “Use this description” to create a synthetic job for tailoring.
   - On a job card, **Select** then **Tailor** to open suggestions, or **Ignore** to hide it from future scrapes.

3. **Suggestions**
   - With a resume and job selected, click **“Generate Suggestions”**.
   - **Apply** or **Reject** suggestions. When you’re done (or not), click **Complete**: the job is added to your ignored list, the suggestions panel clears, and the updated resume stays until you select a new job (then it resets to your default/original).

4. **Log out**
   - Use **Log out** in the header to sign out.

---

## 6. Common issues

- **`ModuleNotFoundError: No module named 'app'` when running uvicorn**  
  Make sure you run `uvicorn` from the `backend/` directory:

  ```bash
  cd backend
  source venv/bin/activate
  uvicorn app.main:app --reload
  ```

- **JWT library syntax error (`jose.py`, missing parentheses in `print`)**  
  This means the wrong `jose` package is installed. Fix by:

  ```bash
  pip uninstall -y jose
  pip install "python-jose[cryptography]"
  ```

- **LLM / parsing / tailoring fails with GOOGLE_API_KEY error**  
  Double‑check that `GOOGLE_API_KEY` is set in `backend/.env` and that `python-dotenv` is installed (it’s in `requirements.txt`).

---

## 7. Running tests (backend)

From `backend/` with venv active:

```bash
pytest
```

There are tests for:

- Parsing (`app/tests/parse_tests.py`)
- Tailoring (`app/tests/tailor_tests.py`)
- Scraping (`app/tests/scrape_tests.py`)
- Auth (`app/tests/auth_tests.py`)

This is my attempt at making internship (or job) searching easier and more fruitful. 
