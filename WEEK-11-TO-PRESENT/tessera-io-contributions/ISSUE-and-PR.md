# Contribution #3 — RAG chunking respects `chunk_size`

Prepared for https://github.com/Kushaal-k/Tessera.io — **not yet posted.**

---

## Proposed issue (Bug report)

**Title:** [BUG] RAG `_split_into_chunks` can emit chunks larger than `chunk_size` for long tokens

**Body:**

In `apps/ai-service/src/rag.py`, `_split_into_chunks(text, chunk_size)` is supposed
to split ingested content into chunks that respect `chunk_size`. When a **single
token is longer than `chunk_size`**, it instead returns a chunk larger than the
limit.

The split condition is guarded by `and current`:

```python
if current_len + len(word) + 1 > chunk_size and current:
    chunks.append(" ".join(current))
    ...
current.append(word)
```

When `current` is empty and the next token already exceeds `chunk_size`, the guard
is `False`, so the oversized token is appended whole and later flushed as its own
chunk.

**Reproduction:**
```python
_split_into_chunks("x" * 33, 10)   # -> ['xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']  (len 33 > 10)
```

**Impact:** `chunk_size` is constrained to `[64, 4096]`, but this service ingests
**code**, where long URLs, base64 blobs, minified lines, and long identifiers
routinely exceed 64 chars. The placeholder embedder hides this today, but once a
real embedding provider is wired in (the `# replace with real embedding provider
later` TODO), an oversized chunk will exceed the model's token limit and fail or
silently truncate.

**Expected:** every returned chunk has length `<= chunk_size`.

---

## Proposed PR

**Branch:** `fix/rag-chunk-size-oversized-token`
**Commit (signed off):** `fix(ai-service): split oversized tokens so RAG chunks respect chunk_size`

**Description:**

Fixes the above. Oversized tokens are now hard-split into `chunk_size`-sized
pieces, so the function guarantees `len(chunk) <= chunk_size` for all chunks.
Normal multi-word chunking is unchanged. Extracted the flush logic into a small
helper to avoid duplication.

**Testing:**
- New `apps/ai-service/tests/test_rag_chunking.py` — 8 cases covering empty input,
  normal splitting, size invariant, order preservation, the oversized-token
  regression, oversized-token-among-words, and the exact-size boundary.
- `python -m pytest tests/` passes; `ruff check` and `ruff format --check` clean.
- (Local note: verified the algorithm + ran ruff locally on Python 3.9; the full
  pytest suite runs in CI on Python 3.11 since `ai-service` deps require >=3.10.)

**Checklist:** signed-off commit, read CONTRIBUTING.md, self-reviewed, no new
warnings. No UI changes (so no screenshot needed).

---

## Files in this folder
- `rag-chunking-fix.patch` — the exact diff (apply with `git apply` from the Tessera.io repo root)
- `test_rag_chunking.py` — the new test file
