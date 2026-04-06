"""
Gemini client wrapper used by DocuBot.

Handles:
- Configuring the Gemini client from the GEMINI_API_KEY environment variable
- Naive generation over the full docs corpus (Phase 0)
- RAG style answers that use only retrieved snippets (Phase 2)
"""

import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None


GEMINI_MODEL_NAME = "gemini-2.5-flash"


class GeminiClient:
    """
    Simple wrapper around the Gemini model.
    """

    def __init__(self):
        if genai is None:
            raise RuntimeError(
                "The google-generativeai package is not installed. "
                "Install dependencies from requirements.txt to enable LLM features."
            )

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY environment variable. "
                "Set it in your shell or .env file to enable LLM features."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    # -----------------------------------------------------------
    # Phase 0: naive generation over full docs
    # -----------------------------------------------------------

    def naive_answer_over_full_docs(self, query, all_text):
        prompt = f"""
You are a documentation assistant helping a developer.

Use only the documentation below to answer the question.
If the documentation does not contain the answer, reply exactly:
"I do not know based on the docs I have."

Documentation:
{all_text}

Developer question:
{query}

When you answer, mention the file names that support your response when possible.
"""
        response = self.model.generate_content(prompt)
        return (response.text or "").strip()

    # -----------------------------------------------------------
    # Phase 2: RAG style generation over retrieved snippets
    # -----------------------------------------------------------

    def answer_from_snippets(self, query, snippets):
        """
        Generate an answer using only the retrieved snippets.
        """
        if not snippets:
            return "I do not know based on the docs I have."

        context_blocks = []
        for filename, text in snippets:
            context_blocks.append(f"File: {filename}\n{text}")

        context = "\n\n".join(context_blocks)

        prompt = f"""
You are a cautious documentation assistant helping developers understand a codebase.

You will receive:
- A developer question
- A small set of retrieved documentation snippets

Your job:
- Answer using only the snippets.
- Do not invent endpoints, variables, or behavior.
- If the snippets are insufficient, reply exactly:
  "I do not know based on the docs I have."

Snippets:
{context}

Developer question:
{query}

If you answer, briefly cite the file names you relied on.
"""

        response = self.model.generate_content(prompt)
        return (response.text or "").strip()
