# DocuBot Model Card

## 1. System Overview

**What is DocuBot trying to do?**

DocuBot is a documentation assistant for developers. Its goal is to answer questions about a small codebase-like document set by either retrieving source text directly or combining retrieval with Gemini in a grounded RAG workflow.

**What inputs does DocuBot take?**

DocuBot takes a user question, the files inside the `docs/` folder, and optionally the `GEMINI_API_KEY` environment variable when LLM features are enabled.

**What outputs does DocuBot produce?**

Depending on the mode, it returns either raw retrieved snippets, a Gemini-generated answer over the full corpus, or a Gemini-generated answer grounded in retrieved snippets.

---

## 2. Retrieval Design

**How does your retrieval system work?**

I used a simple inverted index that maps lowercase tokens to the files where they appear. When a question comes in, DocuBot tokenizes the query, looks up candidate files from the index, scores them with token overlap, and then extracts the strongest matching paragraph from each document as the returned snippet.

**What tradeoffs did you make?**

I chose simplicity over sophistication. The retriever is fast and easy to explain, but it only understands exact token overlap. That means it can miss relevant text when the question uses different wording than the docs.

---

## 3. Use of the LLM (Gemini)

**When does DocuBot call the LLM and when does it not?**

- Naive LLM mode: sends the entire document corpus to Gemini.
- Retrieval only mode: never calls Gemini and only returns source snippets.
- RAG mode: retrieves the top snippets first, then sends only those snippets to Gemini.

**What instructions do you give the LLM to keep it grounded?**

I instruct Gemini to use only the provided documentation, avoid inventing functions or configuration values, cite the supporting file names, and say `"I do not know based on the docs I have."` when the evidence is not sufficient.

---

## 4. Experiments and Comparisons

| Query | Naive LLM: helpful or harmful? | Retrieval only: helpful or harmful? | RAG: helpful or harmful? | Notes |
|------|---------------------------------|--------------------------------------|---------------------------|-------|
| Where is the auth token generated? | Helpful when grounded | Helpful | Helpful | AUTH.md is a strong match |
| How do I connect to the database? | Helpful | Helpful | Helpful | DATABASE.md and SETUP.md both matter |
| Which endpoint lists all users? | Helpful | Helpful | Helpful | API reference is explicit |
| How does a client refresh an access token? | Sometimes over-explains | Helpful | Most helpful | RAG gives a cleaner grounded answer |

**What patterns did you notice?**

Naive LLM mode sounds the most polished, but it is the easiest mode to over-trust. Retrieval only is less fluent but very transparent because I can see the original text. RAG felt like the best balance when the retriever chose the right file first.

---

## 5. Failure Cases and Guardrails

**Describe at least two concrete failure cases you observed.**

Failure case 1:
For questions about topics that never appear in the docs, such as payment processing, retrieval returns nothing useful. The correct behavior is to refuse instead of guessing.

Failure case 2:
Questions that use different wording than the docs can underperform because the retriever depends on exact token overlap. A better system would use embeddings or synonym-aware matching.

**When should DocuBot say "I do not know based on the docs I have"?**

- When no document gets a meaningful retrieval score
- When the snippets mention the topic only indirectly and do not support a confident answer
- When the user asks about a feature that does not exist in the docs

**What guardrails did you implement?**

- Retrieval returns no answer when nothing scores above zero
- RAG only uses the selected snippets instead of the whole corpus
- The Gemini prompt includes an explicit refusal rule
- Gemini import errors fail gracefully so retrieval mode still works

---

## 6. Limitations and Future Improvements

**Current limitations**

1. The retriever relies on exact token overlap.
2. Snippets are selected at the paragraph level instead of semantic chunking.
3. Evaluation checks source-file matches more than final answer quality.

**Future improvements**

1. Add synonym-aware search or embeddings.
2. Rank smaller chunks instead of full documents first.
3. Add stronger automated tests for answer quality and refusal behavior.

---

## 7. Responsible Use

**Where could this system cause real world harm if used carelessly?**

A tool like this could mislead developers if they assume every fluent answer is correct. Wrong documentation answers could lead to broken auth flows, unsafe configuration, or wasted debugging time.

**What instructions would you give real developers who want to use DocuBot safely?**

- Treat answers as a starting point, not as the source of truth.
- Verify important claims against the cited files.
- Prefer retrieval-only mode when accuracy matters more than polish.
- Be cautious when the question is outside the available docs.
