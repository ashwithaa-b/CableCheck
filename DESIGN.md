# CableCheck — System Design

## 1. Project Overview

CableCheck is a Generative AI-powered procurement assistant designed to help engineers analyze technical and commercial information from electrical cable manufacturers.

The system aims to reduce the time spent manually searching annual reports, technical documents, and supplier information.

## 2. Problem Statement

Procurement engineers frequently need to compare suppliers, understand cable specifications, and evaluate manufacturer capabilities.

This information is often scattered across lengthy PDF documents, making manual research time-consuming.

CableCheck aims to simplify this process through AI-powered document retrieval and question answering.

## 3. Proposed Architecture

CableCheck is being developed using the following technologies:

| Component                 | Technology     |
| ------------------------- | -------------- |
| Programming language      | Python 3.12    |
| Backend framework         | FastAPI        |
| Generative AI             | Google Gemini  |
| Database                  | PostgreSQL 16  |
| Vector database extension | pgvector       |
| Containerization          | Docker         |
| Container orchestration   | Docker Compose |
| Automated testing         | Pytest         |
| Code quality              | Ruff           |
| Continuous integration    | GitHub Actions |

## 4. Current System Architecture

The implemented backend follows this flow:

User Request → FastAPI → Gemini API → AI Response → User

The application also supports streaming responses and tracks AI token usage.

The development environment includes PostgreSQL with pgvector for future document retrieval functionality.

## 5. Implemented Features

### 5.1 FastAPI Backend

The application provides REST API endpoints for interacting with CableCheck.

Current endpoints:

* `GET /health` — Checks application health.
* `POST /chat` — Generates AI responses using Gemini.
* `POST /chat/stream` — Streams AI responses.
* `GET /usage` — Retrieves recorded token usage.

### 5.2 Gemini AI Integration

Google Gemini provides the language-model capabilities.

The application supports a configurable primary model and a fallback model.

### 5.3 Streaming Responses

CableCheck supports streaming AI-generated responses to improve the user experience.

### 5.4 Token Usage Tracking

The backend records AI token usage in a local JSONL file.

This provides a foundation for monitoring API consumption and estimating operating costs.

### 5.5 PostgreSQL and pgvector

PostgreSQL 16 is configured through Docker Compose.

The pgvector extension is installed to support future similarity searches using document embeddings.

The database is not yet integrated into the document retrieval pipeline.

### 5.6 Docker Deployment

Docker Compose manages two services:

1. FastAPI application
2. PostgreSQL database

The application can be accessed locally through port `8001` when running through Docker Compose.

## 6. Planned Retrieval-Augmented Generation (RAG) Architecture

The planned document-processing pipeline is:

PDF Documents → Text Extraction → Chunking → Embedding Generation → PostgreSQL/pgvector

The planned question-answering pipeline is:

User Question → Hybrid Search → Relevant Document Chunks → Gemini → Answer with Source References

Hybrid search is intended to combine:

* Keyword-based retrieval (BM25)
* Vector similarity search
* Result reranking

The objective is to improve retrieval accuracy for technical terms such as 400 kV, EHV, and cable specifications.

These RAG components are planned features and are not yet fully implemented.

## 7. Dataset

The initial dataset focuses on annual reports and business responsibility reports from electrical equipment and cable manufacturers.

Target companies include:

* Polycab
* KEI Industries
* Havells
* ABB India
* Siemens India
* Hitachi Energy India

The dataset will support questions about manufacturer capabilities, product portfolios, technical specifications, and procurement-related information.

## 8. Testing and Continuous Integration

CableCheck uses:

* Ruff for Python code-quality checks.
* Pytest for automated testing.
* GitHub Actions for continuous integration.

The CI workflow automatically runs checks when changes are pushed to GitHub.

At the Week 2 milestone, the CI workflow passed successfully.

## 9. Security Considerations

API credentials are stored in environment variables rather than directly in application code.

The `.env` file is excluded from Git tracking.

Future improvements may include authentication, rate limiting, and more detailed API error handling.

## 10. Development Roadmap

### Week 1 — Dataset Preparation

* Identify relevant manufacturers.
* Collect annual reports.
* Develop dataset collection utilities.
* Create an initial dataset manifest.

### Week 2 — Backend Infrastructure

* Integrate Gemini AI.
* Implement streaming responses.
* Track token usage.
* Configure PostgreSQL and pgvector.
* Set up Docker Compose.
* Establish automated testing and CI.

### Week 3 — Document Processing

Planned activities:

* Extract text from PDF documents.
* Split extracted text into searchable chunks.
* Generate document embeddings.
* Store embeddings in PostgreSQL.
* Begin implementing document retrieval.

### Future Development

* Hybrid search with BM25 and vector similarity.
* Retrieval reranking.
* Source-grounded answers.
* Retrieval evaluation using Recall@5.
* Procurement-focused user interface.

## 11. Conclusion

CableCheck provides the backend foundation for an AI-powered procurement research assistant.

The Week 2 milestone establishes the application infrastructure, AI integration, database environment, and automated testing.

The next development phase will focus on transforming manufacturer documents into a searchable knowledge base.
