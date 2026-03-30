import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = sorted(
            self.songs,
            key=lambda song: self._score_song_object(user, song)[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score_song_object(user, song)
        return ", ".join(reasons)

    def _score_song_object(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
            reasons.append("mood match (+1.5)")

        energy_gap = abs(song.energy - user.target_energy)
        energy_score = max(0.0, 1.0 - energy_gap)
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score:.2f})")

        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.5
            reasons.append("matches acoustic preference (+0.5)")
        elif not user.likes_acoustic and song.acousticness <= 0.4:
            score += 0.5
            reasons.append("matches non-acoustic preference (+0.5)")

        return score, reasons


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
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


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    score = 0.0
    reasons: List[str] = []

    if song["genre"].lower() == str(user_prefs.get("genre", "")).lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"].lower() == str(user_prefs.get("mood", "")).lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    target_energy = float(user_prefs.get("energy", 0.5))
    energy_gap = abs(song["energy"] - target_energy)
    energy_score = max(0.0, 1.0 - energy_gap)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    explanation = ", ".join(reasons)
    return score, explanation


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """

    scored_songs: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
