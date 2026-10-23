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

### 1. Document Processing

* Extract text from PDF documents.
* Split documents into searchable chunks.
* Preserve company names, financial years and page numbers.

### 2. Hybrid Search

* BM25 keyword retrieval.
* Vector-based semantic retrieval.
* Combined search results using Reciprocal Rank Fusion.
* Cross-encoder re-ranking.

### 3. AI Question Answering

* Accept natural-language questions.
* Retrieve relevant document passages.
* Generate evidence-based answers.
* Provide PDF citations.

### 4. Exact-Term Highlighting

* Highlight voltage ratings and technical terms.
* Highlight financial segment codes.
* Display relevant source passages.

### 5. Vendor Assessment Agent

* Retrieve manufacturer information.
* Draft vendor assessment memos.
* Generate vendor clarification emails.
* Require procurement manager approval before final saving or sending.

## Example Questions

1. Does KEI Industries manufacture EHV cables, and up to what voltage?
2. What was Polycab's wires and cables segment revenue and margin last year?
3. Which manufacturers report export revenue above 10% of sales?

## Evaluation

CableCheck will compare vector-only retrieval against hybrid retrieval.

**Evaluation dataset:** 60 exact-term questions.

**Primary metric:** Recall@5.

**Target:** 90% or higher.

The evaluation will measure whether relevant supporting passages appear among the top five retrieved results.

## Proposed Technology Stack

* Python
* FastAPI
* PyMuPDF
* Sentence Transformers
* FAISS
* BM25
* Cross-Encoder
* Large Language Model
* Streamlit
* SQLite

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

**Current Phase:** Project setup and dataset collection.

## Live Application

To be added after deployment.
