# CableCheck

**AI-powered cable and switchgear vendor intelligence**

CableCheck is a college Generative AI project for answering procurement and
vendor-research questions using evidence from manufacturers' annual reports.
It combines PDF text extraction, page-aware chunking, vector retrieval, and
Gemini-generated answers with document citations.

## Project status — completed through Week 3

The document-processing and retrieval-augmented generation (RAG) pipeline is
implemented. The `POST /ask` endpoint retrieves report passages from PostgreSQL
with pgvector, supplies them to Gemini, and returns an answer with citations to
the source document and PDF page.

The current retrieval baseline uses SentenceTransformers
(`all-MiniLM-L6-v2`) to embed questions and chunks, then performs semantic
nearest-neighbor search with pgvector. For each matching chunk, it also
retrieves nearby chunks from the same document and PDF page (up to two chunk
IDs on either side). This adds local context; it is not a second search method.

**Hybrid search is planned, not implemented.** BM25 keyword search, reciprocal
rank fusion (RRF), and reranking are not part of the current retrieval
pipeline. Retrieval is semantic vector search only.

## Dataset

Three Polycab India annual reports are currently ingested:

| Report | PDF pages in corpus |
|---|---:|
| FY2023-24 | Included |
| FY2024-25 | Included |
| FY2025-26 | Included |

Together, the corpus contains 1,252 PDF pages and 6,459 document chunks.
KEI Industries reports have not been ingested, so the system should abstain
when those reports are needed.

## Week 3 evaluation

The initial qualitative evaluation covered the 10 questions in
[`docs/QUESTIONS.md`](./docs/QUESTIONS.md). Results are documented in
[`docs/EVAL_v0.md`](./docs/EVAL_v0.md):

| Result | Questions |
|---|---:|
| Full passes | 7 |
| Provisional passes | 2 |
| Partial passes | 1 |

This is a qualitative, question-by-question evaluation, not a statistical
accuracy estimate. No Recall@k or other aggregate retrieval benchmark has
been measured. The provisional results need citation verification; one
partial result exposed an inconsistency in reported financial figures.

## Technology

| Area | Implemented |
|---|---|
| API | Python 3.12, FastAPI, Pydantic |
| PDF processing | pypdf for text extraction with PDF page numbers |
| Chunking and embeddings | Page-aware text chunks; SentenceTransformers `all-MiniLM-L6-v2` |
| Retrieval and storage | PostgreSQL 16, pgvector, Psycopg 3 |
| Answer generation | Google Gemini through the Google GenAI SDK |
| Deployment and checks | Docker Compose, GitHub Actions, pytest, Ruff |

BM25, RRF, reranking, and a user-facing frontend remain planned work.

## API

Run the API locally as described in [Setup](#setup). Interactive API
documentation is available at `http://localhost:8001/docs`.

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Application health |
| `/ready` | GET | PostgreSQL connectivity check |
| `/usage` | GET | Gemini token usage and estimated costs |
| `/chat` | POST | Gemini response to a general message |
| `/chat/stream` | POST | Server-sent event stream from Gemini |
| `/ask` | POST | RAG answer grounded in retrieved report passages |

Example `/ask` request:

```json
{
  "question": "What was Polycab India's W&C segment revenue in FY2024-25?"
}
```

The response contains the question, answer, model, and citations. Citations
are extracted from source references in the generated answer; automatic
claim-to-source verification is not implemented.

## Gemini fallback and retries

The synchronous `/chat` and `/ask` endpoints call the configured primary
Gemini model first and can use the configured fallback model if primary
generation fails. `/ask` also tries the fallback when the primary response is
empty, and avoids a duplicate attempt when both model settings are identical.
Each model attempt uses up to three calls for retryable temporary failures
(selected HTTP errors, timeouts, and connection errors), with exponential
backoff and randomized jitter. Non-retryable errors are not retried.

`/chat/stream` also has a fallback model, but does not use this retry
mechanism: it moves to the fallback if the primary fails before emitting
content. If streaming fails after content has started, it reports an
interrupted stream instead of switching models.

Automated tests mock Gemini; running the test suite does not make Gemini API
calls.

## Setup

### Prerequisites

- Python 3.12
- Docker Desktop with Docker Compose, for the local PostgreSQL/pgvector
  service
- A Gemini API key to use `/chat` and `/ask`

### Install Python packages

The current `requirements.txt` is UTF-16 encoded with a truncated final line,
so pip cannot parse it. It also does not list the RAG dependencies pypdf and
SentenceTransformers. Until the requirements files are corrected, install
the packages directly:

```powershell
python -m pip install fastapi pydantic-settings uvicorn google-genai "psycopg[binary]" python-dotenv pypdf sentence-transformers pytest httpx ruff pre-commit
```

### Configure Gemini

Copy `.env.example` to `.env` and add a valid API key. The model settings are
optional; the application defaults are shown below.

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.6-flash
GEMINI_FALLBACK_MODEL=gemini-3.5-flash-lite
```

Do not commit `.env` or expose API keys.

### Start PostgreSQL and initialize its table

Start only the database service:

```powershell
docker compose up -d db
```

The API code expects a `document_chunks` table but does not currently create
the table or run migrations automatically. Initialize it once in the local
database:

```powershell
docker compose exec db psql -U cablecheck -d cablecheck -c "CREATE EXTENSION IF NOT EXISTS vector; CREATE TABLE IF NOT EXISTS document_chunks (document_name TEXT NOT NULL, page_number INTEGER NOT NULL, chunk_id INTEGER NOT NULL, content TEXT NOT NULL, embedding VECTOR(384), PRIMARY KEY (document_name, page_number, chunk_id));"
```

Set `DATABASE_URL` in the same shell in which you run the API or ingestion
script:

```powershell
$env:DATABASE_URL = "postgresql://cablecheck:cablecheck_local@localhost:5432/cablecheck"
```

### Ingest reports and run the API

From the repository root, run the idempotent ingestion script to parse PDFs
from `data/raw/polycab`, split text into chunks, generate embeddings, and store
them in PostgreSQL:

```powershell
python -m app.rag.ingest
```

Then start the API:

```powershell
uvicorn app.main:app --reload --port 8001
```

The application is available at `http://localhost:8001`; use
`http://localhost:8001/docs` to explore its endpoints. `/ask` requires both a
configured Gemini API key and a populated, reachable database.

**Docker API note:** The current Dockerfile installs only `requirements.txt`,
which pip cannot parse as described above and which omits the RAG packages.
Therefore the full API image is not a verified setup path at this milestone;
the Compose PostgreSQL service can be used with the local Python API steps
above.

## Tests and pre-commit

Run the automated tests and repository pre-commit checks:

```powershell
python -m pytest -q
pre-commit run --all-files
```

**Week 3 test result:** 24 passed.

The test suite covers API behavior, Gemini fallback and retry behavior,
database readiness, usage tracking, and document search. Gemini calls are
mocked.

## Limitations and Week 4 improvements

Current limitations:

- Retrieval uses semantic similarity only; there are no company, fiscal-year,
  reporting-basis, or metric filters.
- Citation extraction does not establish that each citation supports the
  specific claim next to it.
- The Q5 citation support and Q9 EHV-manufacturing coverage need verification.
- Q10 exposed a financial-grounding issue: related revenue and total-income
  figures need clearer metric, reporting-basis, and source treatment.
- The ten-question evaluation is qualitative; no retrieval benchmark has been
  run.
- Only Polycab reports are ingested; questions about other manufacturers
  cannot yet be answered from their reports.
- The dependency manifest and Docker API build path need correction before
  setup is reproducible from a clean environment.

Planned Week 4 work:

1. Verify the citations and report evidence for Q5 and Q9, and re-check each
   figure and accounting basis in Q10.
2. Improve retrieval with company, year, reporting-basis, and metric metadata
   or filters.
3. Add claim-to-source checks for financial figures and labels.
4. Define a repeatable evaluation with source passages and citation checks
   before reporting retrieval metrics.
5. Improve clean-environment installation and Docker setup; expand the corpus
   before evaluating other manufacturers.
6. Implement and evaluate BM25, reciprocal-rank fusion, and reranking as
   planned retrieval enhancements.

## Deployment

The API has been deployed to Render at
[cablecheck.onrender.com](https://cablecheck.onrender.com). The free service
may sleep when inactive. Local PostgreSQL connectivity is implemented, but a
cloud PostgreSQL connection has not been confirmed; consequently, deployed
`/ask` functionality depends on database configuration not yet verified.

## Repository

[GitHub: ashwithaa-b/CableCheck](https://github.com/ashwithaa-b/CableCheck)
