"""
Sanity checks for Playlist Chaos logic.

I wrote this as a lightweight alternative to pytest so anyone can run it quickly:

    python sanity_checks.py
"""

from playlist_logic import build_playlists, classify_song, compute_playlist_stats, normalize_song, search_songs, lucky_pick, DEFAULT_PROFILE


def test_classification_rules():
    profile = dict(DEFAULT_PROFILE)
    profile["hype_min_energy"] = 7
    profile["chill_max_energy"] = 3
    profile["favorite_genre"] = "rock"

    # Hype by energy
    s = normalize_song({"title": "X", "artist": "Y", "genre": "pop", "energy": 7})
    assert classify_song(s, profile) == "Hype"

    # Hype by favorite genre
    s = normalize_song({"title": "X", "artist": "Y", "genre": "rock", "energy": 2})
    assert classify_song(s, profile) == "Hype"

    # Hype by keyword in genre
    s = normalize_song({"title": "X", "artist": "Y", "genre": "punk", "energy": 5})
    assert classify_song(s, profile) == "Hype"

    # Chill by energy
    s = normalize_song({"title": "X", "artist": "Y", "genre": "pop", "energy": 3})
    assert classify_song(s, profile) == "Chill"

    # Chill by keyword in title
    s = normalize_song({"title": "ambient dreams", "artist": "Y", "genre": "pop", "energy": 9})
    assert classify_song(s, profile) == "Chill"

    # Mixed otherwise
    s = normalize_song({"title": "X", "artist": "Y", "genre": "pop", "energy": 5})
    assert classify_song(s, profile) == "Mixed"


def test_search_partial_case_insensitive():
    songs = [
        normalize_song({"title": "Thunderstruck", "artist": "AC/DC", "genre": "rock", "energy": 9}),
        normalize_song({"title": "Hello", "artist": "Adele", "genre": "pop", "energy": 5}),
    ]
    res = search_songs(songs, "ac", field="artist")
    assert len(res) == 1 and res[0]["artist"] == "ac/dc"


def test_stats_math():
    profile = dict(DEFAULT_PROFILE)
    songs = [
        {"title": "A", "artist": "X", "genre": "rock", "energy": 9},  # hype
        {"title": "B", "artist": "Y", "genre": "ambient", "energy": 1},  # chill
        {"title": "C", "artist": "Z", "genre": "pop", "energy": 5},  # mixed
    ]
    playlists = build_playlists(songs, profile)
    stats = compute_playlist_stats(playlists)
    assert stats["total_songs"] == 3
    assert abs(stats["avg_energy"] - (9 + 1 + 5) / 3) < 1e-9
    assert abs(stats["hype_ratio"] - (stats["hype_count"] / 3)) < 1e-9


def test_lucky_pick_empty_safe():
    assert lucky_pick({"Hype": [], "Chill": [], "Mixed": []}, mode="hype") is None


if __name__ == "__main__":
    test_classification_rules()
    test_search_partial_case_insensitive()
    test_stats_math()
    test_lucky_pick_empty_safe()
    print("All sanity checks passed.")
