import json
from pathlib import Path
from typing import Dict, List


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_listening_guides(json_path: str = "data/listening_guides.json") -> Dict:
    path = Path(json_path)
    if not path.exists():
        path = _project_root() / json_path

    with path.open(encoding="utf-8") as infile:
        return json.load(infile)


def normalize_preferences(user_prefs: Dict) -> Dict:
    genre = str(user_prefs.get("genre", "")).strip().lower()
    mood = str(user_prefs.get("mood", "")).strip().lower()
    energy = float(user_prefs.get("energy", 0.5))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    return {
        "genre": genre,
        "mood": mood,
        "energy": max(0.0, min(1.0, energy)),
        "likes_acoustic": likes_acoustic,
    }


def validate_user_preferences(user_prefs: Dict, knowledge_base: Dict) -> Dict:
    normalized = normalize_preferences(user_prefs)
    allowed_genres = set(knowledge_base["genres"].keys())
    allowed_moods = set(knowledge_base["moods"].keys())
    warnings: List[str] = []

    if normalized["genre"] not in allowed_genres:
        warnings.append(
            f"Genre '{normalized['genre']}' is outside the classroom knowledge base, so the system will rely more on mood and energy."
        )

    if normalized["mood"] not in allowed_moods:
        warnings.append(
            f"Mood '{normalized['mood']}' is not explicitly modeled, so results may be less reliable."
        )

    raw_energy = float(user_prefs.get("energy", 0.5))
    if raw_energy != normalized["energy"]:
        warnings.append("Energy was clipped into the supported 0.0 to 1.0 range.")

    if normalized["energy"] < 0.15 or normalized["energy"] > 0.95:
        warnings.append("Extreme energy requests usually reduce recommendation confidence in this small dataset.")

    return {
        "normalized": normalized,
        "warnings": warnings,
    }


def retrieve_song_candidates(user_prefs: Dict, songs: List[Dict], limit: int = 6) -> List[Dict]:
    candidates: List[Dict] = []
    for song in songs:
        evidence: List[str] = []
        if song["genre"].lower() == user_prefs["genre"]:
            evidence.append("retrieved for exact genre")
        elif user_prefs["genre"] and user_prefs["genre"] in song["genre"].lower():
            evidence.append("retrieved for related genre")

        if song["mood"].lower() == user_prefs["mood"]:
            evidence.append("retrieved for exact mood")

        if abs(song["energy"] - user_prefs["energy"]) <= 0.18:
            evidence.append("retrieved for close energy")

        if user_prefs["likes_acoustic"] and song["acousticness"] >= 0.60:
            evidence.append("retrieved for acoustic preference")
        elif not user_prefs["likes_acoustic"] and song["acousticness"] <= 0.40:
            evidence.append("retrieved for non-acoustic preference")

        if evidence:
            candidates.append({"song": song, "evidence": evidence})

    if not candidates:
        ordered = sorted(
            songs,
            key=lambda item: abs(item["energy"] - user_prefs["energy"]),
        )
        return [{"song": song, "evidence": ["fallback retrieval using energy proximity"]} for song in ordered[:limit]]

    candidates.sort(
        key=lambda item: (
            -len(item["evidence"]),
            abs(item["song"]["energy"] - user_prefs["energy"]),
            item["song"]["title"],
        )
    )
    return candidates[:limit]


def retrieve_context_snippets(user_prefs: Dict, knowledge_base: Dict) -> List[Dict]:
    snippets: List[Dict] = []

    genre_entry = knowledge_base["genres"].get(user_prefs["genre"])
    if genre_entry:
        snippets.append(
            {
                "source": f"genre:{user_prefs['genre']}",
                "snippet": genre_entry["summary"],
            }
        )

    mood_entry = knowledge_base["moods"].get(user_prefs["mood"])
    if mood_entry:
        snippets.append(
            {
                "source": f"mood:{user_prefs['mood']}",
                "snippet": mood_entry["summary"],
            }
        )

    acoustic_key = "acoustic" if user_prefs["likes_acoustic"] else "studio"
    snippets.append(
        {
            "source": f"preference:{acoustic_key}",
            "snippet": knowledge_base["preferences"][acoustic_key],
        }
    )

    return snippets
