import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
)


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_reads_catalog():
    songs = load_songs(str(PROJECT_ROOT / "data" / "songs.csv"))

    assert len(songs) == 10
    assert songs[0]["title"] == "Sunrise City"
    assert isinstance(songs[0]["energy"], float)


def test_recommend_songs_returns_scores_and_explanations():
    songs = load_songs(str(PROJECT_ROOT / "data" / "songs.csv"))
    user_prefs = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=3)

    assert len(recommendations) == 3
    top_song, top_score, explanation = recommendations[0]
    assert top_song["genre"] == "lofi"
    assert top_song["mood"] == "chill"
    assert top_score > 0
    assert "energy" in explanation.lower()
