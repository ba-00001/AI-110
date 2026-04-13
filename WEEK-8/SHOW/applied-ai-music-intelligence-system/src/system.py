import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .recommender import load_songs, score_song
from .retrieval import (
    load_listening_guides,
    retrieve_context_snippets,
    retrieve_song_candidates,
    validate_user_preferences,
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _build_logger() -> logging.Logger:
    logs_dir = _project_root() / "logs"
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("music_intelligence_system")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(logs_dir / "system.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    return logger


@dataclass
class Recommendation:
    title: str
    artist: str
    score: float
    confidence: float
    explanation: str
    retrieval_evidence: List[str]


class MusicIntelligenceSystem:
    def __init__(
        self,
        songs_path: str = "data/songs.csv",
        guides_path: str = "data/listening_guides.json",
    ):
        self.songs = load_songs(songs_path)
        self.knowledge_base = load_listening_guides(guides_path)
        self.logger = _build_logger()

    def run(self, user_prefs: Dict, k: int = 3) -> Dict:
        validation = validate_user_preferences(user_prefs, self.knowledge_base)
        normalized = validation["normalized"]
        retrieved_candidates = retrieve_song_candidates(normalized, self.songs, limit=max(k * 2, 5))
        retrieved_context = retrieve_context_snippets(normalized, self.knowledge_base)

        scored_recommendations: List[Recommendation] = []
        for candidate in retrieved_candidates:
            song = candidate["song"]
            score, reasons = score_song(normalized, song)
            confidence = self._estimate_confidence(normalized, song, candidate["evidence"], validation["warnings"])
            reasons.extend([f"evidence: {item}" for item in candidate["evidence"]])

            scored_recommendations.append(
                Recommendation(
                    title=song["title"],
                    artist=song["artist"],
                    score=score,
                    confidence=confidence,
                    explanation="; ".join(reasons),
                    retrieval_evidence=candidate["evidence"],
                )
            )

        scored_recommendations.sort(key=lambda item: (-item.score, -item.confidence, item.title))
        selected = scored_recommendations[:k]
        overall_confidence = round(
            sum(item.confidence for item in selected) / max(len(selected), 1),
            2,
        )

        result = {
            "request": normalized,
            "warnings": validation["warnings"],
            "retrieved_context": retrieved_context,
            "recommendations": [item.__dict__ for item in selected],
            "overall_confidence": overall_confidence,
        }

        self.logger.info("system_run=%s", json.dumps(result))
        return result

    def _estimate_confidence(
        self,
        user_prefs: Dict,
        song: Dict,
        retrieval_evidence: List[str],
        warnings: List[str],
    ) -> float:
        confidence = 0.45

        if song["genre"].lower() == user_prefs["genre"]:
            confidence += 0.2
        if song["mood"].lower() == user_prefs["mood"]:
            confidence += 0.15
        if abs(song["energy"] - user_prefs["energy"]) <= 0.10:
            confidence += 0.1
        if len(retrieval_evidence) >= 3:
            confidence += 0.08
        if warnings:
            confidence -= 0.1

        return round(max(0.1, min(0.99, confidence)), 2)
