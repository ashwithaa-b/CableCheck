# 10 Real Questions My User Will Ask

## Target User

Procurement engineer at a Chennai-based EPC contractor
evaluating cable and switchgear manufacturers.

## Dataset Available

Currently, CableCheck contains Polycab India annual reports for:

- FY2023-24
- FY2024-25
- FY2025-26

Questions about KEI Industries are included to test whether
the RAG system correctly identifies missing information
instead of generating unsupported answers.

## Questions

| # | Question | Where the answer is (document, page) | Needs more than one page? |
|---|---|---|---|
| 1 | Does KEI Industries manufacture EHV cables, and up to what voltage rating? | KEI Industries Annual Report (not yet ingested) | No |
| 2 | Does Polycab India manufacture 400 kV EHV cables? | Polycab Annual Report, page to be identified | No |
| 3 | What cable manufacturing capacities are reported by KEI Industries? | KEI Industries Annual Report (not yet ingested) | Yes |
| 4 | What are Polycab India's major business segments? | Polycab Annual Report FY2024-25, page to be identified | No |
| 5 | What products are included in Polycab India's Wires & Cables segment? | Polycab Annual Report FY2024-25, page to be identified | Yes |
| 6 | What was Polycab India's W&C segment revenue in FY2024-25? | Polycab Annual Report FY2024-25, page to be identified | No |
| 7 | What was Polycab India's W&C segment profit margin in FY2024-25? | Polycab Annual Report FY2024-25, page to be identified | Yes |
| 8 | How did Polycab India's W&C segment revenue change between FY2023-24 and FY2024-25? | Polycab Annual Reports FY2023-24 and FY2024-25, pages to be identified | Yes |
| 9 | What does Polycab India report about its EHV cable business? | Polycab Annual Reports, pages to be identified | Yes |
| 10 | What was Polycab India's total revenue in FY2024-25? | Polycab Annual Report FY2024-25, page to be identified | No |

## Evaluation Plan

### Document-Grounded Questions

Questions 2, 4, 5, 6, 7, 8, 9, and 10 evaluate:

- Retrieval accuracy
- Factual correctness
- Citation accuracy
- Financial information extraction
- Multi-page information retrieval

### Hallucination Prevention Questions

Questions 1 and 3 evaluate whether CableCheck correctly
refuses to generate unsupported information about KEI Industries.

Expected answer when relevant documents are unavailable:

"The provided documents do not contain enough information."

### Evaluation Status

| Question | Status |
|---|---|
| Q1 | PASS |
| Q2 | PASS |
| Q3 | PASS |
| Q4 | PENDING |
| Q5 | PENDING |
| Q6 | PASS |
| Q7 | PASS |
| Q8 | PENDING |
| Q9 | PENDING |
| Q10 | PENDING |

## Current Progress

- Total Questions: 10
- Passed: 5
- Pending: 5
- Blocked: 0

## Future Dataset Expansion

CableCheck will eventually include annual reports from:

1. Polycab India
2. KEI Industries
3. Havells India
4. ABB India
5. Siemens Ltd
6. Hitachi Energy India

After ingestion, CableCheck will be evaluated on
cross-company comparisons and procurement-related questions.
