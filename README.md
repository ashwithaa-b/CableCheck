# GENAI PROJECT: CABLECHECK

## Project Title

**CableCheck — AI-Powered Cable and Switchgear Vendor Intelligence System**

## Problem

Procurement engineers working in Engineering, Procurement and Construction (EPC) companies need accurate technical and financial information about cable and switchgear manufacturers before selecting vendors.

Important information such as product specifications, voltage ratings, manufacturing capabilities, revenue, profit margins and export performance is often available only in lengthy annual reports and Business Responsibility and Sustainability Reports (BRSRs).

Manually searching these documents is time-consuming. Traditional semantic search systems may also fail to distinguish exact technical terms such as "400 kV", "EHV", "W&C" and "FMEG".

CableCheck aims to solve this problem using Generative AI and hybrid information retrieval.

## Who It Is For

* Procurement engineers working in EPC companies.
* Electrical engineers evaluating cable and switchgear manufacturers.
* Vendor assessment and supply chain teams.
* Technical professionals researching manufacturers' products and financial performance.

## Project Objective

To develop an AI-powered application that retrieves accurate technical and financial information from manufacturers' annual reports and BRSRs.

The system will allow users to ask natural-language questions and receive evidence-based answers with document citations.

## Signature Feature

**Exact-Term Highlighter**

CableCheck will highlight important technical terms, voltage ratings and financial segment codes within retrieved PDF snippets.

For example, when a user searches for "400 kV EHV cables", the system will identify and highlight the matching technical terms in the supporting document.

Each answer will include the source document and page number.

## Hardest Problem

**Exact-Term Hybrid Search and Re-Ranking**

Traditional vector search retrieves information based on semantic similarity but may return incorrect results for questions involving exact voltage ratings, technical codes or financial terminology.

CableCheck will address this challenge by combining:

1. BM25 keyword search.
2. Vector-based semantic search.
3. Reciprocal Rank Fusion.
4. Cross-encoder re-ranking.
5. Custom tokenization for technical terms.

The system will preserve important terms such as "400 kV", "EHV", "W&C" and "FMEG" during keyword indexing and retrieval.

Retrieval performance will be evaluated using a 60-question exact-term test dataset.

## Dataset

The project will use annual reports and BRSRs published by six electrical equipment manufacturers.

| Company              | Documents                | Period  |
| -------------------- | ------------------------ | ------- |
| Polycab India        | Annual Reports and BRSRs | 3 years |
| KEI Industries       | Annual Reports and BRSRs | 3 years |
| Havells India        | Annual Reports and BRSRs | 3 years |
| ABB India            | Annual Reports and BRSRs | 3 years |
| Siemens Ltd          | Annual Reports and BRSRs | 3 years |
| Hitachi Energy India | Annual Reports and BRSRs | 3 years |

**Target dataset:** At least 18 annual reports and 6,000 pages.

Documents will be collected from the manufacturers' official investor relations websites.

Document counts, page counts and applicable usage terms will be recorded after collection.

## Key Features

### 1. Document Processing (Planned)

* Extract text from PDF documents.
* Split documents into searchable chunks.
* Preserve company names, financial years and page numbers.

### 2. Hybrid Search (Planned)

* BM25 keyword retrieval.
* Vector-based semantic retrieval.
* Combined search results using Reciprocal Rank Fusion.
* Cross-encoder re-ranking.

### 3. AI Question Answering

* Accept natural-language questions.
* Generate responses using Google Gemini.
* Support primary and fallback AI models.
* Provide streaming responses.

**Planned enhancements:**

* Retrieve relevant document passages.
* Generate evidence-based answers.
* Provide PDF citations.

### 4. Exact-Term Highlighting (Planned)

* Highlight voltage ratings and technical terms.
* Highlight financial segment codes.
* Display relevant source passages.

### 5. Vendor Assessment Agent (Planned)

* Retrieve manufacturer information.
* Draft vendor assessment memos.
* Generate vendor clarification emails.
* Require procurement manager approval before final saving or sending.

## Example Questions

1. Does KEI Industries manufacture EHV cables, and up to what voltage?
2. What was Polycab's wires and cables segment revenue and margin last year?
3. Which manufacturers report export revenue above 10% of sales?

These questions represent the intended RAG functionality. Document-grounded answers will be supported after the retrieval pipeline is implemented.

## Evaluation

CableCheck will compare vector-only retrieval against hybrid retrieval.

**Evaluation dataset:** 60 exact-term questions.

**Primary metric:** Recall@5.

**Target:** 90% or higher.

The evaluation will measure whether relevant supporting passages appear among the top five retrieved results.

## Technology Stack

### Currently Implemented

* Python 3.12
* FastAPI
* Google Gemini API
* Google GenAI Python SDK
* Pydantic
* PostgreSQL 16
* pgvector Docker image
* Psycopg 3
* Docker
* Docker Compose
* pytest
* GitHub Actions
* Render

### Planned Technologies

* PyMuPDF
* Sentence Transformers
* BM25
* FAISS or pgvector-based vector retrieval
* Cross-Encoder
* Streamlit or another suitable frontend framework

## Week 2 — Backend Development and Deployment

CableCheck's Week 2 implementation establishes the backend infrastructure required for future document retrieval and AI-powered vendor intelligence.

### Implemented Features

* FastAPI REST API.
* Google Gemini AI integration.
* Primary and fallback Gemini models.
* Streaming response endpoint.
* Token usage tracking.
* Thinking-token tracking.
* Estimated API cost calculations.
* PostgreSQL 16 with pgvector.
* Docker and Docker Compose.
* Health and database readiness endpoints.
* Automated testing with pytest.
* GitHub Actions continuous integration.
* Cloud deployment using Render.

**In progress:** Exponential-backoff retries with jitter.

### API Endpoints

| Endpoint       | Method | Description                           |
| -------------- | ------ | ------------------------------------- |
| `/health`      | GET    | Application health check              |
| `/ready`       | GET    | PostgreSQL database readiness         |
| `/usage`       | GET    | Token usage and estimated API costs   |
| `/chat`        | POST   | Gemini AI question answering          |
| `/chat/stream` | POST   | Streaming Gemini responses            |
| `/docs`        | GET    | Interactive Swagger API documentation |

### Local Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/ashwithaa-b/CableCheck.git
cd CableCheck
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Create a `.env` file using `.env.example` as a template.

Example:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.6-flash
GEMINI_FALLBACK_MODEL=gemini-3.5-flash-lite
```

Replace `your_api_key` with a valid Gemini API key.

**Security:** Never commit `.env` files or API keys to GitHub.

## Docker Setup

CableCheck uses Docker Compose to run the FastAPI backend and PostgreSQL database.

### Build and Start Containers

```bash
docker compose up -d --build
```

### Check Container Status

```bash
docker compose ps
```

Expected services:

* `cablecheck-api` — FastAPI application.
* `cablecheck-db` — PostgreSQL database.

### Stop Containers

```bash
docker compose down
```

### Restart Containers

```bash
docker compose up -d
```

### Local Application URLs

| Service            | URL                          |
| ------------------ | ---------------------------- |
| API Documentation  | http://localhost:8001/docs   |
| Health Check       | http://localhost:8001/health |
| Database Readiness | http://localhost:8001/ready  |
| API Usage          | http://localhost:8001/usage  |

### PostgreSQL Configuration

The Docker Compose setup includes:

* PostgreSQL 16.
* pgvector-enabled PostgreSQL image.
* Persistent database volume.
* Database health checks.
* FastAPI-to-PostgreSQL connectivity.

The application connects to PostgreSQL using the `DATABASE_URL` environment variable.

## Database Readiness Testing

The `/ready` endpoint checks whether PostgreSQL is available.

### Database Available

Expected response:

```json
{
  "status": "ready",
  "database": "connected"
}
```

HTTP status: `200 OK`

### Database Unavailable

Stop PostgreSQL:

```bash
docker compose stop db
```

Check:

`http://localhost:8001/ready`

Expected response:

```json
{
  "detail": "Database is unavailable"
}
```

HTTP status: `503 Service Unavailable`

Restart PostgreSQL:

```bash
docker compose start db
```

**Verification:** Both database availability and failure handling have been tested successfully using Docker.

## Automated Testing

CableCheck uses pytest for automated backend testing.

### Run Tests

```bash
python -m pytest -q
```

### Latest Verified Results

```text
14 passed, 2 warnings
```

The two warnings are dependency deprecation warnings and do not represent test failures.

### Test Coverage Areas

* Application health checks.
* API cost calculations.
* Token usage recording.
* Token usage summaries.
* Database readiness.
* Database connection failure handling.
* Missing Gemini API key.
* Successful Gemini responses.
* Primary model failure and fallback.
* Gemini API failure handling.

Gemini API calls are mocked during automated tests to avoid unnecessary API requests and costs.

## Gemini API Integration

CableCheck uses Google Gemini for AI-generated responses.

### Primary Model

`gemini-3.6-flash`

### Fallback Model

`gemini-3.5-flash-lite`

The application attempts to use the primary model first.

If the primary model fails, it attempts the configured fallback model.

If both models fail, the application returns an error response.

### Planned Reliability Improvement

* Exponential-backoff retry logic.
* Randomized jitter.
* Additional retry-specific automated tests.

## Token Usage and Cost Tracking

CableCheck records AI usage information, including:

* Request timestamp.
* Model name.
* Input tokens.
* Output tokens.
* Thinking tokens.
* Total tokens.
* Estimated API cost.

Usage records are stored locally in:

`data/usage.jsonl`

### Cost Estimation

The application estimates costs using configured model pricing.

For `gemini-3.6-flash`, the currently configured rates are:

| Token Type                 | Price per 1 Million Tokens |
| -------------------------- | -------------------------- |
| Input                      | $0.75                      |
| Output, including thinking | $3.75                      |

These are configured estimates and should be checked against current provider pricing.

Models without verified pricing are reported with unknown estimated cost rather than an invented value.

For additional information, see:

`docs/COST.md`

**Note:** Usage records stored on an ephemeral cloud filesystem may be lost when the service restarts or redeploys.

## Live Application — Render

CableCheck has been deployed to Render.

### Live API

https://cablecheck.onrender.com

### Interactive API Documentation

https://cablecheck.onrender.com/docs

### Health Endpoint

https://cablecheck.onrender.com/health

### Usage Endpoint

https://cablecheck.onrender.com/usage

### Deployment Notes

* The application runs as a Render web service.
* The deployment uses the free service tier.
* Free services may sleep during inactivity.
* The first request after inactivity may take additional time.
* Environment variables must be configured securely in Render.
* GitHub Actions is used for continuous integration.

**Database limitation:** A PostgreSQL connection has been verified locally through Docker Compose. A cloud PostgreSQL connection has not yet been confirmed.

The `/ready` endpoint requires `DATABASE_URL` and returns HTTP 503 if the database is not configured or cannot be reached.

The Render health check should continue using `/health` until a cloud database is configured.

## Development Plan

### Weeks 1–6: Retrieval and Question Answering

* Collect company reports.
* Extract PDF text.
* Build a vector search baseline.
* Implement BM25 and hybrid search.
* Add re-ranking and exact-term highlighting.
* Evaluate retrieval accuracy.

### Weeks 7–12: AI Agent

* Build vendor assessment workflows.
* Generate assessment memos.
* Draft vendor clarification emails.
* Implement manager approval.
* Test the complete system.

## Project Status

### Week 1 — Project Setup and Dataset Collection

* Project repository created.
* Initial documentation prepared.
* Dataset collection tools added.
* Annual report collection initiated.

### Week 2 — Backend Infrastructure

* FastAPI backend implemented.
* Gemini API integrated.
* Primary and fallback models configured.
* Streaming endpoint implemented.
* Token usage tracking added.
* Estimated cost calculation added.
* PostgreSQL connectivity implemented.
* Docker Compose configured.
* Database failure handling verified.
* 14 automated tests passing.
* Render deployment established.

**Remaining Week 2 work:**

* Implement exponential-backoff retries with jitter.
* Complete final code-quality checks.
* Commit and push the latest changes.
* Verify the final GitHub Actions run.

### Week 3 — Planned

* PDF text extraction.
* Document chunking.
* Embedding generation.
* Vector database integration.
* Retrieval-augmented generation (RAG).

## Repository

GitHub: https://github.com/ashwithaa-b/CableCheck

## Security Notes

* Keep API keys in environment variables.
* Do not commit `.env` files.
* Use mock API responses in automated tests.
* Do not expose database credentials in public repositories.
* Use secure database credentials for production deployments.
