# Progress

Commit after every class. Tag every Friday: `git tag week-N && git push origin week-N`.

## Week 1 (tag week-1 by Fri 23 Oct)

- [ ] Repo created from the Examate template and registered on the form (registration to verify)
- [x] README top section filled from my project card
- [x] /health runs locally
- [x] docs/QUESTIONS.md: 10 real questions
- [x] 50+ pages collected (1,252 pages)
- [x] DATASET.md completed
- [x] data/manifest.csv generated
- [x] Three synthetic TXT samples created in data/sample/
- [ ] Confirm sample file format meets submission requirements
- [x] Tag week-1 pushed

## Week 2 (tag week-2 by Fri 30 Oct)

- [x] POST /chat calls an LLM and returns structured JSON
- [x] Streaming endpoint implemented
- [x] Timeouts, retries and fallback model implemented for /chat
- [ ] Verify retry and fallback behaviour for streaming
- [x] Cost log + GET /usage
- [x] Docker Compose (API + Postgres/pgvector) runs locally
- [x] CI green
- [x] Application deployed on Render
- [x] Live link included in README
- [x] Tag week-2 pushed

### Week 2 Submission Note

The week-2 tag points to commit 422b937.

Additional Week 2 improvements were pushed to main after the tag:

- b20540c: System architecture documentation
- 91fcf4c: Gemini retries, cost tracking, database readiness and tests

The existing week-2 tag has been preserved.

## Week 3 (tag week-3 by Fri 6 Nov)

- [ ] Parser keeps page numbers and headings
- [ ] 500+ pages chunked, embedded and stored in pgvector
- [ ] POST /ask answers with [document, page] citations
- [ ] docs/EVAL_v0.md with my 10 questions scored
- [ ] Tag week-3 pushed

## Daily log

| Date | What I did today | Commit |
|---|---|---|
| 2026-10-23 | Collected three Polycab annual reports and prepared dataset documentation | See Git history |
| 2026-10-30 | Week 2 submission tagged | 422b937 |
| 2026-11-03 | Verified Week 1 and Week 2 files and Git tags | Verification only |
