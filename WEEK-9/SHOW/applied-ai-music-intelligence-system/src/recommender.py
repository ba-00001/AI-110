import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


MOOD_TARGETS = {
    "happy": {"valence": 0.85, "danceability": 0.80},
    "chill": {"valence": 0.60, "danceability": 0.55},
    "relaxed": {"valence": 0.70, "danceability": 0.50},
    "focused": {"valence": 0.58, "danceability": 0.58},
    "moody": {"valence": 0.45, "danceability": 0.65},
    "intense": {"valence": 0.50, "danceability": 0.75},
}


@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _normalize(text: str) -> str:
    return text.strip().lower()


def _similarity_score(value: float, target: float, weight: float) -> float:
    return max(0.0, 1.0 - abs(value - target)) * weight


def _genre_score(preferred_genre: str, song_genre: str) -> Tuple[float, str]:
    preferred = _normalize(preferred_genre)
    song_value = _normalize(song_genre)

    if not preferred or not song_value:
        return 0.0, ""

    if preferred == song_value:
        return 3.0, "exact genre match (+3.0)"

    preferred_tokens = set(preferred.split())
    song_tokens = set(song_value.split())
    if preferred_tokens & song_tokens:
        return 1.5, "related genre match (+1.5)"

    return 0.0, ""


def _acoustic_preference_score(likes_acoustic: bool, acousticness: float) -> Tuple[float, str]:
    if likes_acoustic and acousticness >= 0.60:
        bonus = round(0.75 + (acousticness - 0.60) * 0.75, 2)
        return bonus, f"fits an acoustic leaning vibe (+{bonus:.2f})"
    if not likes_acoustic and acousticness <= 0.40:
        bonus = round(0.75 + (0.40 - acousticness) * 0.40, 2)
        return bonus, f"fits a polished studio vibe (+{bonus:.2f})"
    return 0.0, ""


def _song_as_dict(song: Song) -> Dict:
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = sorted(
            self.songs,
            key=lambda song: self._score_song_object(user, song)[0],
            reverse=True,
        )
        return scored_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score_song_object(user, song)
        return "; ".join(reasons)

    def _score_song_object(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score, reasons = score_song(
            {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            _song_as_dict(song),
        )
        return score, reasons


def load_songs(csv_path: str) -> List[Dict]:
    path = Path(csv_path)
    if not path.exists():
        path = Path(__file__).resolve().parents[1] / csv_path

    songs: List[Dict] = []
    with path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []

    genre_score, genre_reason = _genre_score(
        str(user_prefs.get("genre", "")),
        str(song.get("genre", "")),
    )
    score += genre_score
    if genre_reason:
        reasons.append(genre_reason)

    preferred_mood = _normalize(str(user_prefs.get("mood", "")))
    song_mood = _normalize(str(song.get("mood", "")))
    if preferred_mood and preferred_mood == song_mood:
        score += 2.0
        reasons.append("exact mood match (+2.0)")

    target_energy = float(user_prefs.get("energy", 0.50))
    energy_score = _similarity_score(float(song.get("energy", 0.0)), target_energy, 2.0)
    score += energy_score
    reasons.append(f"energy is close to the target (+{energy_score:.2f})")

    mood_targets = MOOD_TARGETS.get(preferred_mood)
    if mood_targets:
        valence_score = _similarity_score(
            float(song.get("valence", 0.0)),
            mood_targets["valence"],
            0.75,
        )
        dance_score = _similarity_score(
            float(song.get("danceability", 0.0)),
            mood_targets["danceability"],
            0.50,
        )
        score += valence_score + dance_score
        reasons.append(f"valence fits the mood target (+{valence_score:.2f})")
        reasons.append(f"danceability supports the mood (+{dance_score:.2f})")

    if "likes_acoustic" in user_prefs:
        acoustic_score, acoustic_reason = _acoustic_preference_score(
            bool(user_prefs["likes_acoustic"]),
            float(song.get("acousticness", 0.0)),
        )
        score += acoustic_score
        if acoustic_reason:
            reasons.append(acoustic_reason)

    return round(score, 3), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    scored_songs: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda item: (-item[1], item[0]["title"]))
    return scored_songs[:k]
