# GENAI PROJECT: CABLECHECK

## Problem

People who work with technical cables and electrical wiring may struggle to identify cable-related issues, understand technical specifications, and find the correct information from documentation. Searching through lengthy technical documents can take time and lead to confusion. CableCheck aims to use Generative AI to make cable-related information easier to access and understand. It is designed to help users obtain clear, relevant answers to their cable-related questions.

## Who it is for

- Electrical and Electronics Engineering (ECE) students who need help understanding cable specifications and technical documentation.
- Electrical technicians and engineers who need to retrieve cable-related information efficiently.

## Signature feature

A GenAI-powered question-answering interface that helps users retrieve and understand cable-related technical information using natural-language questions.

## Hardest problem (my interview story)

The hardest problem was designing a reliable way for users to get relevant answers to cable-related questions. The system needs to interpret the user's question, identify relevant information, and present an understandable response. Ensuring that answers are relevant to the available technical information, rather than misleading or unsupported, is an important challenge.

## Dataset

| **Source** | **Link** | **Documents** | **Pages** | **Licence / terms** |
| ---------- | -------- | ------------- | --------- | ------------------- |
| To be confirmed from the actual project dataset | Add the original source URL | To be counted | To be counted | Verify the source licence and usage terms |

## 10 real questions

See [docs/QUESTIONS.md](https://github.com/ashwithaa-b/CableCheck/blob/main/docs/QUESTIONS.md).

## Run it

```bash
python -m venv .venv
```

**Windows:**
```powershell
.venv\Scripts\activate
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Check the health endpoint:
```bash
curl localhost:8000/health
```

## Live link

To be added in Week 2.
