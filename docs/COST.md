# CableCheck — Gemini API Cost Tracking

## 1. Overview

CableCheck uses the Google Gemini API to answer user questions.

The application tracks token usage and estimates API costs in USD.

## 2. Models

Primary model: gemini-3.6-flash

Fallback model: gemini-3.5-flash-lite

## 3. API Pricing

The following paid-tier rates are used for Gemini 3.6 Flash
through December 31, 2026:

| Token Type | Cost per 1 Million Tokens |
|------------|---------------------------|
| Input tokens | $0.75 |
| Output tokens (including thinking) | $3.75 |

Fallback model pricing has not yet been verified.

## 4. Cost Calculation

Estimated Cost (USD) =

(Input Tokens × 0.75 +
(Output Tokens + Thinking Tokens) × 3.75) / 1,000,000

## 5. Example Calculation

Input tokens: 2

Output tokens: 9

Thinking tokens: 144

Estimated cost:

(2 × 0.75 + 153 × 3.75) / 1,000,000

Result: $0.00057525

## 6. Usage Tracking

CableCheck records:

- Timestamp
- Gemini model
- Input tokens
- Output tokens
- Thinking tokens
- Total tokens
- Estimated cost in USD

Usage records are stored in:

data/usage.jsonl

The GET /usage endpoint returns aggregated usage information.

## 7. Limitations

- Costs are estimates based on configured paid-tier rates.
- Actual billing may differ because of free-tier usage,
  pricing changes, or other billing conditions.
- Fallback model costs remain unknown until pricing is verified.
- Older usage records may underestimate costs because
  thinking tokens were not recorded separately.
- Usage records are stored locally and may not persist
  across cloud service restarts.
- The implementation does not yet cover every possible
  Gemini billing category.
