# DocuBot

DocuBot is a small documentation assistant that helps answer developer questions about a codebase. I built it to compare three different approaches to AI-assisted question answering:

1. **Naive LLM mode**
   Sends the full documentation corpus to Gemini and asks for an answer.

2. **Retrieval only mode**
   Uses a small inverted index and a scoring function to pull the most relevant snippets without calling an LLM.

3. **RAG mode**
   Retrieves the most relevant snippets first, then asks Gemini to answer using only those snippets.

The docs in `docs/` are a mock codebase reference set, so I can experiment with retrieval and grounding without needing a real backend service.

<img src="https://github.com/user-attachments/assets/2423d15f-b4ca-44c5-bd50-3f69fb93624a" alt="screenshot 1" width="600" />

---

## What I Changed

In my version of the project, I implemented the missing retrieval system in `docubot.py`:

- document loading with a fallback in-memory corpus
- tokenization and a tiny inverted index
- document scoring based on query overlap
- snippet extraction so retrieval returns the strongest section instead of the full file

I also improved `llm_client.py` so that:

- LLM imports fail gracefully when Gemini is unavailable
- naive mode actually sends the full docs to the model
- RAG mode explicitly tells Gemini to stay grounded in the retrieved snippets

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the example file:

```bash
copy .env.example .env
```

Then edit `.env` with your Gemini API key if you want to use modes 1 and 3:

```env
GEMINI_API_KEY=your_api_key_here
```

If you do not set a Gemini key, retrieval only mode still works.

---

## Running DocuBot

```bash
python main.py
```

Mode options:

- `1` = Naive LLM over the full docs
- `2` = Retrieval only
- `3` = RAG

You can press Enter to run the built-in sample queries or type your own question.

---

## Running Evaluation

The retrieval evaluation checks whether the retrieved files match the expected source documents for the sample questions.

```bash
python evaluation.py
```

I also added pytest coverage for the retrieval pipeline:

```bash
pytest
```

---

## What I Observed

Retrieval only mode was the most reliable when the answer existed clearly in one document because it showed the source text directly. Naive LLM mode felt more fluent, but that fluency only helps when the model stays grounded. RAG worked best when the retriever selected the right snippet first, because it combined grounding with a cleaner natural-language answer.

The biggest lesson for me was that retrieval quality matters a lot. If the wrong document is chosen, the LLM step cannot magically fix the underlying evidence problem.

---

## Limitations

- The retriever uses simple token overlap, so it does not understand synonyms or deeper meaning.
- Snippet selection is paragraph-based, which works for this dataset but would be weak on larger docs.
- The project depends on Gemini for modes 1 and 3, so those paths are unavailable without an API key.
- The evaluation is lightweight and only checks approximate source matches, not full answer quality.

---

## Files I Focused On

- `docubot.py`
- `llm_client.py`
- `evaluation.py`
- `dataset.py`
- `tests/test_docubot.py`
