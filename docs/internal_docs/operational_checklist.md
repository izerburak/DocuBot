# Operations Checklist (Internal)

## Before Demo
- [ ] Local LLM runtime running (model loaded)
- [ ] Documents folder populated
- [ ] Index built and retrieval returns >0 chunks
- [ ] API health endpoint returns OK
- [ ] Rate limit enabled (optional for demo)
- [ ] Logging set to INFO (not DEBUG) to avoid leaking prompts

## During Demo
- [ ] Watch latency (LLM + retrieval)
- [ ] If answer seems off, increase top_k temporarily
- [ ] If LLM hangs, restart LLM runtime first

## After Demo
- [ ] Clear temporary logs (if containing user content)
- [ ] Export demo metrics (requests count, avg latency)
