"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import glob
import os
import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

from dataset import load_fallback_documents

TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")
STOPWORDS = {
    "a",
    "all",
    "an",
    "and",
    "any",
    "are",
    "based",
    "by",
    "does",
    "do",
    "docs",
    "for",
    "how",
    "i",
    "in",
    "is",
    "it",
    "mention",
    "of",
    "on",
    "or",
    "the",
    "there",
    "these",
    "this",
    "to",
    "what",
    "where",
    "which",
}
TOKEN_NORMALIZATIONS = {
    "connect": "connection",
    "connected": "connection",
    "created": "generate",
    "fields": "field",
    "generated": "generate",
    "generation": "generate",
    "lists": "list",
    "processing": "process",
    "required": "require",
}


class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        self.documents = self.load_documents()
        self.index = self.build_index(self.documents)
        self._document_lookup: Dict[str, str] = {
            filename: text for filename, text in self.documents
        }

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self) -> List[Tuple[str, str]]:
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        Falls back to the in-memory sample corpus if the folder is missing.
        """
        docs: List[Tuple[str, str]] = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as file_handle:
                    text = file_handle.read()
                filename = os.path.basename(path)
                docs.append((filename, text))

        if not docs:
            return load_fallback_documents()

        docs.sort(key=lambda item: item[0])
        return docs

    # -----------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------

    def _normalize_token(self, token: str) -> str:
        return TOKEN_NORMALIZATIONS.get(token, token)

    def _tokenize(self, text: str) -> List[str]:
        return [
            self._normalize_token(token)
            for token in TOKEN_PATTERN.findall(text.lower())
            if token not in STOPWORDS
        ]

    def _best_snippet(self, query: str, text: str) -> str:
        blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
        if not blocks:
            return text.strip()

        ranked_blocks = sorted(
            blocks,
            key=lambda block: self.score_document(query, block),
            reverse=True,
        )
        best_block = ranked_blocks[0]
        if self.score_document(query, best_block) == 0:
            return blocks[0]
        return best_block

    # -----------------------------------------------------------
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def build_index(self, documents):
        """
        Build a tiny inverted index mapping lowercase words to the documents
        they appear in.
        """
        index = defaultdict(set)
        for filename, text in documents:
            for token in set(self._tokenize(text)):
                index[token].add(filename)
        return {token: sorted(filenames) for token, filenames in index.items()}

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
    # -----------------------------------------------------------

    def score_document(self, query, text):
        """
        Return a simple relevance score for how well the text matches the query.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return 0

        token_counts = Counter(self._tokenize(text))
        unique_matches = sum(1 for token in query_tokens if token_counts.get(token, 0) > 0)
        frequency_bonus = sum(token_counts.get(token, 0) for token in query_tokens) * 0.1
        score = (unique_matches * 2) + frequency_bonus

        normalized_query = query.strip().lower()
        if normalized_query and normalized_query in text.lower():
            score += len(query_tokens) + 2

        return score

    def retrieve(self, query, top_k=3):
        """
        Use the index and scoring function to select top_k relevant document snippets.

        Returns a list of (filename, snippet) sorted by score descending.
        """
        query_tokens = list(dict.fromkeys(self._tokenize(query)))
        candidate_filenames = set()

        for token in query_tokens:
            candidate_filenames.update(self.index.get(token, []))

        if candidate_filenames:
            candidate_docs = [
                (filename, self._document_lookup[filename])
                for filename in candidate_filenames
            ]
        else:
            candidate_docs = self.documents

        scored_results = []
        for filename, text in candidate_docs:
            document_score = self.score_document(query, text)
            if document_score <= 0:
                continue

            snippet = self._best_snippet(query, text)
            total_score = document_score + self.score_document(query, snippet)
            scored_results.append((filename, snippet, total_score))

        scored_results.sort(key=lambda item: (-item[2], item[0]))
        return [(filename, snippet) for filename, snippet, _ in scored_results[:top_k]]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive generation over the full corpus.
        """
        return "\n\n".join(
            f"File: {filename}\n{text}" for filename, text in self.documents
        )
