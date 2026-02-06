# FAQ

## Does the assistant browse the internet?
No. This demo is offline and uses only local documents (if RAG is enabled) plus the local model.

## Why does it sometimes answer without citations?
If retrieval returns no relevant chunks or citations are disabled, the assistant may respond without references.

## How do I improve accuracy?
- Add higher quality documents
- Reindex after changes
- Increase `top_k`
- Reduce chunk size if docs are long

## Is user data stored?
By default, the demo should not persist chat history unless explicitly enabled in configuration.
