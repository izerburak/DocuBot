# Risk Register (Internal)

| ID | Risk | Category | Impact | Mitigation | Status |
|---|---|---|---|---|---|
| R-001 | Prompt injection through user messages | LLM | Medium | System prompt rules + context isolation | Active |
| R-002 | Sensitive doc leakage via retrieval | RAG/Data | High | Access control + redaction + doc tagging | Planned |
| R-003 | Hallucinated outputs presented as facts | LLM | Medium | "Cite or say unknown" policy | Active |
| R-004 | Reindex endpoint abused | API/Security | Medium | Admin-only + rate limit | Planned |
