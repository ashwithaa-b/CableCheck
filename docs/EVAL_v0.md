# CableCheck — RAG Evaluation v0

## 1. Evaluation Overview

**Project:** CableCheck
**Evaluation stage:** Week 3
**Evaluation date:** 4 November 2026
**Status:** Complete; includes provisional and partial-pass results

### Objective

Evaluate CableCheck's ability to retrieve information from annual reports,
abstain when relevant company documents are absent, produce grounded answers,
perform financial calculations, and cite supporting PDF pages.

## 2. Dataset and System

The evaluation corpus contains Polycab India annual reports for FY2023-24,
FY2024-25, and FY2025-26. KEI Industries reports have not been ingested.
The corpus comprises 1,252 PDF pages and 6,459 document chunks.

CableCheck uses FastAPI, PostgreSQL with pgvector, the
`all-MiniLM-L6-v2` embedding model, and Gemini for answer generation. Search
uses semantic vector similarity (`top_k=5`) and nearby chunks from the same
document page. Citations identify a source document and PDF page.

## 3. Evaluation Methodology

The ten questions in `QUESTIONS.md` were evaluated against their intended
behavior and the available annual-report evidence:

- For companies whose reports are absent, check that CableCheck abstains
  rather than asserting unsupported facts.
- For Polycab questions, review the answer against report excerpts, including
  the financial year, reporting basis, metric, calculations, and cited pages
  where applicable.
- Mark citation-dependent answers provisional when their supporting passages
  have not been fully verified.
- Record known errors and uncertainty explicitly; a provisional or partial
  result is not counted as a full pass.

This is a qualitative, question-by-question evaluation. No aggregate retrieval
metric such as Recall@5 was measured, and the results should not be read as a
statistical accuracy estimate.

## 4. Results

| Q# | Question | Observed result | Status |
|---|---|---|---|
| Q1 | Does KEI Industries manufacture EHV cables, and up to what voltage rating? | Correctly abstained because KEI reports are not ingested. | PASS |
| Q2 | Does Polycab India manufacture 400 kV EHV cables? | Cautiously abstained from claiming Polycab manufactures 400 kV EHV cables without sufficient evidence. | PASS |
| Q3 | What cable manufacturing capacities are reported by KEI Industries? | Correctly abstained because KEI reports are not ingested. | PASS |
| Q4 | What are Polycab India's major business segments? | Correctly identified Wires & Cables, FMEG, and EPC. | PASS |
| Q5 | What products are included in Polycab India's Wires & Cables segment? | Identified W&C products; citation support has not been fully verified. | PROVISIONAL PASS |
| Q6 | What was Polycab India's W&C segment revenue in FY2024-25? | Correctly reported W&C revenue with standalone and consolidated bases distinguished. | PASS |
| Q7 | What was Polycab India's W&C segment profit margin in FY2024-25? | Correctly calculated the FY2024-25 standalone W&C operating margin as approximately 13.44%. | PASS |
| Q8 | How did Polycab India's W&C segment revenue change between FY2023-24 and FY2024-25? | Correctly compared W&C revenue and reported consolidated and standalone growth. | PASS |
| Q9 | What does Polycab India report about its EHV cable business? | Correctly cited EHV cable laying by the EPC division; may have missed evidence about EHV cable manufacturing. | PROVISIONAL PASS |
| Q10 | What was Polycab India's total revenue in FY2024-25? | Distinguished consolidated revenue, originally reported standalone revenue, and restated standalone revenue. However, the consolidated total-income figure was inconsistent, and the standalone segment total-income figure was inadequately explained. | PARTIAL PASS |

### Outcome Counts

- **Full passes:** 7/10
- **Provisional passes:** 2/10
- **Partial passes:** 1/10
- **Not evaluated:** 0/10

Provisional and partial results are not counted as full passes. Therefore, the
evaluation does not support a claim that all ten questions passed.

## 5. Financial Results and Known Accuracy Issue

### Question 7: Standalone W&C Operating Margin

CableCheck calculated the FY2024-25 standalone W&C operating margin as:

`(Segment operating results / segment total income) × 100 ≈ 13.44%`

The answer was assessed as correct.

### Question 10: Total Revenue

The answer correctly distinguished consolidated revenue, originally reported
standalone revenue, and restated standalone revenue. It did not consistently
ground all related income figures:

- It gave consolidated total income as **₹224,608.84 million**, rather than the
  FY2024-25 audited consolidated total income of **₹226,159.49 million**.
- It included a standalone segment total-income figure without adequately
  explaining its scope or how it related to company-level total income.

Accordingly, Q10 is a **partial pass**, not a full pass. Revenue from
operations, total income, and segment total income are distinct metrics and
should be labeled and supported separately.

## 6. Key Findings and Remaining Limitations

- Abstention worked for questions requiring KEI reports that are absent from
  the corpus.
- The system answered several Polycab segment and financial questions
  successfully, including a standalone operating-margin calculation.
- Citation support remains unverified for Q5. Q9 may conflate or incompletely
  cover EHV cable laying and EHV cable manufacturing.
- Q10 shows that identifying multiple accounting bases is not sufficient:
  answers must also preserve the metric and scope of each figure, and explain
  reported versus restated comparatives using source evidence.
- Semantic retrieval can return neighboring, similarly worded, or wrong-period
  passages. Company, year, reporting basis, and metric are not currently
  enforced as structured filters.
- No quantitative retrieval benchmark was run; this report makes no Recall@k
  or general accuracy claim.

## 7. Improvements Implemented During Week 3

- Added PDF parsing that preserves document names and PDF page numbers, plus
  chunking and pgvector-backed embedding ingestion and search.
- Added neighboring-chunk retrieval so answer-bearing text split across chunks
  is more likely to reach the prompt.
- Improved `/ask` handling so a failed or empty primary Gemini response can
  use the configured fallback, while avoiding a duplicate call when both
  model settings are identical.
- Added failure-stage/model logging for generation failures and regression
  tests for fallback and retrieval behavior.
- Improved citation extraction for grouped source references and duplicate
  citations from the same page.
- Added general answer instructions to distinguish revenue from operations
  from total income, standalone from consolidated reporting, and reported
  from restated comparatives. The instructions also require figure-specific
  citations and prohibit explaining a restatement beyond the supplied text.

## 8. Next Steps

1. Verify Q5 citations against the cited report pages and claims.
2. Re-evaluate Q9 with separate checks for EHV cable laying and EHV cable
   manufacturing; expand report evidence if needed.
3. Re-run Q10 and verify every reported figure against its exact source,
   including whether it is company-level or segment-level and reported or
   restated.
4. Improve retrieval using document/company, fiscal-year, reporting-basis, and
   metric metadata or filters where available.
5. Add claim-to-source validation for financial values and labels, and ensure
   citations support the specific claims they accompany.
6. Create a repeatable evaluation set with source passages and citation checks;
   measure retrieval metrics only after defining and running that benchmark.
7. Ingest additional manufacturers' reports before evaluating questions that
   require those companies' evidence.

## 9. Conclusion

The evaluation has seven full passes, two provisional passes, and one partial
pass. CableCheck demonstrated useful abstention and several successful
document-grounded answers, but Q5 and Q9 still need citation or coverage
verification, and Q10 exposes remaining financial-grounding errors. These
results are a qualitative evaluation of the ten listed questions, not a
generalized accuracy score.
