"""
Rule based mood analyzer for short text snippets.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from dataset import NEGATIVE_WORDS, POSITIVE_WORDS


class MoodAnalyzer:
    """
    A lightweight rule based mood classifier for short, informal text.
    """

    NEGATION_WORDS = {"not", "never", "no", "isnt", "wasnt", "dont", "didnt", "cant"}
    CONTRAST_WORDS = {"but", "though", "although"}
    STRONG_POSITIVE = {"love", "amazing", "awesome", "best", "beautiful"}
    STRONG_NEGATIVE = {"hate", "terrible", "awful", "worst", "crying"}
    EMOJI_SCORES = {
        ":)": 1,
        ":-)": 1,
        ":(": -1,
        ":-(": -1,
        "lol": 1,
        "ugh": -1,
    }

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS
        self.positive_words = {w.lower() for w in positive_words}
        self.negative_words = {w.lower() for w in negative_words}

    def preprocess(self, text: str) -> List[str]:
        """
        Normalize short text into lowercase tokens while preserving emoticons.
        """
        cleaned = text.strip().lower()
        cleaned = cleaned.replace("'", "")
        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)
        return re.findall(r":-\)|:\)|:-\(|:\(|[a-z0-9]+", cleaned)

    def _score_tokens(self, tokens: List[str]) -> Dict[str, object]:
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        notes: List[str] = []
        positive_total = 0
        negative_total = 0
        negate_next = False
        after_contrast = False

        for token in tokens:
            if token in self.CONTRAST_WORDS:
                after_contrast = True
                notes.append(f"contrast:{token}")
                continue

            if token in self.NEGATION_WORDS:
                negate_next = True
                notes.append(f"negation:{token}")
                continue

            token_score = 0
            if token in self.EMOJI_SCORES:
                token_score = self.EMOJI_SCORES[token]
            elif token in self.positive_words:
                token_score = 2 if token in self.STRONG_POSITIVE else 1
            elif token in self.negative_words:
                token_score = -2 if token in self.STRONG_NEGATIVE else -1

            if token_score == 0:
                negate_next = False
                continue

            if negate_next:
                token_score *= -1
                notes.append(f"flipped:{token}")
                negate_next = False

            if after_contrast:
                token_score += 1 if token_score > 0 else -1
                notes.append(f"contrast-weight:{token}")

            score += token_score

            if token_score > 0:
                positive_hits.append(token)
                positive_total += token_score
            else:
                negative_hits.append(token)
                negative_total += abs(token_score)

        # A tiny sarcasm heuristic for a common breaker pattern.
        if "love" in tokens and ("traffic" in tokens or "stuck" in tokens):
            score -= 2
            negative_total += 2
            notes.append("sarcasm-heuristic:love+traffic")

        return {
            "score": score,
            "positive_hits": positive_hits,
            "negative_hits": negative_hits,
            "positive_total": positive_total,
            "negative_total": negative_total,
            "notes": notes,
        }

    def score_text(self, text: str) -> int:
        """
        Compute a mood score using vocabulary, negation, and contrast handling.
        """
        tokens = self.preprocess(text)
        result = self._score_tokens(tokens)
        return int(result["score"])

    def predict_label(self, text: str) -> str:
        """
        Convert the numeric score into positive, negative, neutral, or mixed.
        """
        tokens = self.preprocess(text)
        result = self._score_tokens(tokens)
        score = int(result["score"])
        positive_total = int(result["positive_total"])
        negative_total = int(result["negative_total"])

        if positive_total > 0 and negative_total > 0:
            if abs(positive_total - negative_total) <= 1:
                return "mixed"
            if score >= 2:
                return "positive"
            if score <= -2:
                return "negative"
            return "mixed"

        if score >= 1:
            return "positive"
        if score <= -1:
            return "negative"
        return "neutral"

    def explain(self, text: str) -> str:
        """
        Return a short explanation for the model decision.
        """
        tokens = self.preprocess(text)
        result = self._score_tokens(tokens)
        return (
            f"tokens={tokens}; score={result['score']}; "
            f"positive={result['positive_hits'] or []}; "
            f"negative={result['negative_hits'] or []}; "
            f"notes={result['notes'] or []}"
        )
