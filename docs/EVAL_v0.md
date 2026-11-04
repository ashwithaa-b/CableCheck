# CableCheck — RAG Evaluation v0

## 1. Evaluation Overview

**Project:** CableCheck  
**Evaluation stage:** Week 3  
**Evaluation date:** 4 November 2026  
**Status:** In Progress

### Objective

Evaluate CableCheck's ability to retrieve information from annual reports, generate grounded answers, perform financial calculations, and provide accurate PDF citations.

## 2. Dataset

Currently ingested:

| Company | Annual Reports |
|---|---|
| Polycab India | FY2024, FY2025, FY2026 |

**Total PDF pages:** 1,252  
**Total document chunks:** 6,459

Other manufacturers' annual reports have not yet been ingested.

## 3. System Configuration

- Backend: FastAPI
- Database: PostgreSQL + pgvector
- Embedding model: all-MiniLM-L6-v2
- Answer generation: Gemini
- Retrieval: Semantic vector similarity
- Retrieval configuration: top_k=5, with neighboring chunks
- Citation format: Document filename and PDF page number

## 4. Evaluation Results

| Q# | Question Topic | Expected Behavior | Observed Result | Status |
|---|---|---|---|---|
| Q1 | KEI EHV cable voltage rating | Abstain without KEI evidence | Correct abstention, no citations | PASS |
| Q2 | Polycab 400 kV EHV cables | Avoid unsupported claims | Abstained, cited FY2026 p18 | PASS |
| Q3 | KEI manufacturing capacities | Abstain without KEI evidence | HTTP 502 during generation | BLOCKED |
| Q4 | ABB switchgear products | Abstain without ABB evidence | Not tested | PENDING |
| Q5 | Siemens electrical products | Abstain without Siemens evidence | Not tested | PENDING |
| Q6 | Polycab W&C segment revenue | Correct figures and citations | Correct standalone and consolidated figures | PASS |
| Q7 | Polycab W&C operating margin | Correct calculation and citation | 13.44% standalone margin | PASS |
| Q8 | KEI FY2025 revenue | Abstain without KEI evidence | Not tested | PENDING |
| Q9 | Export revenue comparison | Abstain without all required reports | Not tested | PENDING |
| Q10 | Hitachi Energy FY2025 revenue | Abstain without Hitachi evidence | Not tested | PENDING |

### Current Results

- Total evaluation questions: 10
- Passed: 4
- Blocked: 1
- Pending: 5
- Completed evaluations: 4/10

These results do not represent an overall accuracy score because six questions have not been successfully evaluated.

## 5. Verified Financial Answers

### Question 6: Polycab Wires and Cables Revenue

**Financial year:** FY2024-25

| Reporting Basis | Revenue (INR Million) | PDF Page |
|---|---:|---:|
| Consolidated | 187,575.07 | 318 |
| Standalone | 184,072.48 | 409 |

Additional standalone segment information:

- External sales: INR 185,459.27 million
- Inter-segment revenue: INR 3,415.72 million
- Total segment income: INR 188,874.99 million
- Supporting PDF page: 427

**Result:** PASS

### Question 7: Polycab Operating Profit Margin

**Reporting basis:** Standalone  
**Financial year:** FY2024-25

Segment operating results: INR 25,386.59 million

Segment total income: INR 188,874.99 million

Operating Margin (%) =
(Segment Operating Results / Segment Total Income) × 100

= (25,386.59 / 188,874.99) × 100

**Operating Margin = 13.44%**

**Source:** polycab_fy2025_annual-report.pdf, PDF page 427

**Result:** PASS

## 6. Citation Validation

CableCheck supports source references such as:

- [Source 5]
- [Source 7, Source 8]
- [Source 9, Source 10]

Grouped citation extraction was corrected during Week 3.

The live API successfully returned the supporting pages:

- PDF page 427
- PDF page 318
- PDF page 409

Duplicate citations from the same PDF page are removed.

## 7. Known Issues

### Issue 1: HTTP 502 on Question 3

Question:

"What cable manufacturing capacities are reported by KEI Industries?"

Observed response:

`Unable to generate a document-grounded answer`

Status: Unresolved.

The failure occurs after retrieval, within the answer-generation or response-processing stage.

The exact exception has not yet been captured.

Diagnostic logging has been added to app/main.py.

### Issue 2: Missing Manufacturer Reports

Only Polycab annual reports are currently ingested.

Questions involving KEI, ABB, Siemens, and Hitachi Energy cannot yet be answered using company-specific evidence.

### Issue 3: Retrieval Limitations

Current retrieval uses semantic vector similarity without company-specific metadata filtering.

Queries about manufacturers absent from the dataset may retrieve unrelated Polycab passages.

### Issue 4: Output Formatting

Some PowerShell responses display incorrect Unicode characters for the rupee symbol.

The cause has not yet been confirmed.

## 8. Automated Tests

Latest reported test result:

**17 passed**

Additional targeted retry tests:

**3 passed**

## 9. Next Steps

1. Diagnose and resolve Question 3's HTTP 502 error.
2. Complete evaluation of Questions 4, 5, 8, 9, and 10.
3. Add a regression test for grouped citation extraction.
4. Improve company-specific retrieval filtering.
5. Ingest the remaining manufacturers' annual reports.
6. Update this report with final evaluation results.
7. Commit the completed Week 3 work.
8. Create and push the Week 3 Git tag.

## 10. Conclusion

CableCheck has demonstrated successful document retrieval, grounded financial question answering, operating-margin calculation, and PDF citation generation.

Four evaluation questions have passed.

The Week 3 evaluation remains incomplete because one question is blocked by an HTTP 502 error and five questions have not yet been tested.