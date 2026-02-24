"""
Playlist Chaos — fixed + heavily commented version.

I’m keeping this file intentionally readable for a debugging / Copilot activity.

Key goals (matches the assignment "Intended Behavior"):
- Reliable mood classification (Hype / Chill / Mixed) using profile thresholds + keywords.
- Consistent normalization (trim whitespace, lowercase artist/genre for comparisons).
- Search should be case-insensitive and partial-match the chosen field (query contained in value).
- Stats should be computed over *unique* songs, with correct averages and ratios.
- Lucky Pick should respect the selected mode and never crash on empty playlists.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

Song = Dict[str, object]
PlaylistMap = Dict[str, List[Song]]

DEFAULT_PROFILE: Dict[str, object] = {
    "name": "Default",
    "hype_min_energy": 7,
    "chill_max_energy": 3,
    "favorite_genre": "rock",
    "include_mixed": True,
}


# -----------------------------
# Normalization helpers
# -----------------------------
def normalize_title(title: str) -> str:
    """
    Normalize a song title for comparisons / display.

    What I care about here:
    - strip leading/trailing whitespace so "Thunderstruck " and "Thunderstruck" match
    - keep original casing (titles look nicer as-entered), but comparisons can lower() later
    """
    if not isinstance(title, str):
        return ""
    return title.strip()


def normalize_artist(artist: str) -> str:
    """
    Normalize an artist name for comparisons.

    I lowercase artists so searches/dupe checks are consistent:
    "AC/DC" == "ac/dc" == " AC/DC "
    """
    if not isinstance(artist, str):
        return ""
    return artist.strip().lower()


def normalize_genre(genre: str) -> str:
    """
    Normalize a genre for comparisons.

    Genres are used for keyword matching + favorite_genre matching, so I force lowercase.
    """
    if not isinstance(genre, str):
        return ""
    return genre.strip().lower()


def normalize_song(raw: Song) -> Song:
    """
    Return a normalized song dict with expected keys.

    Expected shape:
      { title:str, artist:str, genre:str, energy:int, tags:list[str] }

    This function is the "single source of truth" for cleaning user input so the rest
    of the app can assume consistent data.
    """
    title = normalize_title(str(raw.get("title", "")))
    artist = normalize_artist(str(raw.get("artist", "")))
    genre = normalize_genre(str(raw.get("genre", "")))

    # Energy should be an int (1..10 in UI), but I still harden it here.
    energy = raw.get("energy", 0)
    if isinstance(energy, str):
        try:
            energy = int(energy)
        except ValueError:
            energy = 0
    if isinstance(energy, float):
        energy = int(energy)

    # Tags can come in as "a,b,c" or a list — normalize to list[str].
    tags = raw.get("tags", [])
    if tags is None:
        tags = []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    if not isinstance(tags, list):
        tags = [str(tags)]
    tags = [str(t).strip() for t in tags if str(t).strip()]

    return {
        "title": title,
        "artist": artist,
        "genre": genre,
        "energy": int(energy),
        "tags": tags,
    }


# -----------------------------
# Mood engine
# -----------------------------
def classify_song(song: Song, profile: Dict[str, object]) -> str:
    """
    Return a mood label given a song and user profile.

    Intended rules (benchmark):
    - Hype if:
        energy >= hype_min_energy
        OR genre matches favorite_genre
        OR genre contains hype keywords (rock, punk, party)
    - Chill if:
        energy <= chill_max_energy
        OR title contains chill keywords (lofi, ambient, sleep)
    - Mixed otherwise

    Overlap handling (deterministic):
    - If the *title* contains a chill keyword, I classify it as **Chill** first.
      (This keeps "lofi / ambient / sleep" tracks from being forced into Hype just
       because someone typed a high energy value.)
    """
    energy = int(song.get("energy", 0) or 0)

    # Song fields are expected normalized already, but I’m defensive anyway.
    genre = str(song.get("genre", "") or "").lower()
    title = str(song.get("title", "") or "").lower()

    hype_min_energy = int(profile.get("hype_min_energy", 7) or 7)
    chill_max_energy = int(profile.get("chill_max_energy", 3) or 3)
    favorite_genre = str(profile.get("favorite_genre", "") or "").lower().strip()

    hype_keywords = ["rock", "punk", "party"]
    chill_keywords = ["lofi", "ambient", "sleep"]

    is_hype_keyword = any(k in genre for k in hype_keywords)
    is_chill_keyword = any(k in title for k in chill_keywords)

    # 1) Title-based chill keywords take priority (strong signal).
    if is_chill_keyword:
        return "Chill"

    # 2) Hype rules.
    if energy >= hype_min_energy or (favorite_genre and genre == favorite_genre) or is_hype_keyword:
        return "Hype"

    # 3) Energy-based chill rule.
    if energy <= chill_max_energy:
        return "Chill"

    return "Mixed"


def build_playlists(songs: List[Song], profile: Dict[str, object]) -> PlaylistMap:
    """
    Group songs into playlists based on mood + profile.

    I always return all 3 keys so the UI can safely index them.
    """
    playlists: PlaylistMap = {"Hype": [], "Chill": [], "Mixed": []}

    for song in songs:
        normalized = normalize_song(song)
        mood = classify_song(normalized, profile)

        # I store the computed mood on the song so UI and history can display it.
        normalized["mood"] = mood
        playlists[mood].append(normalized)

    return playlists


# -----------------------------
# Utility helpers
# -----------------------------
def merge_playlists(a: PlaylistMap, b: PlaylistMap) -> PlaylistMap:
    """
    Merge two playlist maps into a new map.

    Fix: The original implementation reused list objects (mutating the original),
    which could cause confusing duplicates or state issues.
    """
    merged: PlaylistMap = {}
    for key in set(list(a.keys()) + list(b.keys())):
        merged[key] = list(a.get(key, [])) + list(b.get(key, []))
    return merged


def _song_key(song: Song) -> Tuple[str, str, int]:
    """
    Build a stable "uniqueness" key for stats.

    I’m using (title, artist, energy). You could also include genre, but title+artist
    is usually the identity; energy is included to keep it deterministic if a user
    enters the same song twice with different energy values.
    """
    title = normalize_title(str(song.get("title", "")))
    artist = normalize_artist(str(song.get("artist", "")))
    energy = int(song.get("energy", 0) or 0)
    return (title.lower(), artist.lower(), energy)


def compute_playlist_stats(playlists: PlaylistMap) -> Dict[str, object]:
    """
    Compute statistics across all playlists.

    Intended rules:
    - Total Songs: unique count across all categories
    - Average Energy: average over all unique songs
    - Hype Ratio: hype_count / total_songs
    """
    all_songs: List[Song] = []
    for songs in playlists.values():
        all_songs.extend(songs)

    # De-duplicate for stats to avoid weirdness if something ends up merged twice.
    unique: Dict[Tuple[str, str, int], Song] = {}
    for song in all_songs:
        unique[_song_key(song)] = song

    unique_songs = list(unique.values())

    hype = playlists.get("Hype", [])
    chill = playlists.get("Chill", [])
    mixed = playlists.get("Mixed", [])

    total = len(unique_songs)
    hype_ratio = (len(hype) / total) if total > 0 else 0.0

    avg_energy = 0.0
    if total > 0:
        total_energy = sum(int(song.get("energy", 0) or 0) for song in unique_songs)
        avg_energy = total_energy / total

    top_artist, top_count = most_common_artist(unique_songs)

    return {
        "total_songs": total,
        "hype_count": len(hype),
        "chill_count": len(chill),
        "mixed_count": len(mixed),
        "hype_ratio": hype_ratio,
        "avg_energy": avg_energy,
        "top_artist": top_artist,
        "top_artist_count": top_count,
    }


def most_common_artist(songs: List[Song]) -> Tuple[str, int]:
    """Return the most common artist and count (based on normalized artist)."""
    counts: Dict[str, int] = {}
    for song in songs:
        artist = normalize_artist(str(song.get("artist", "")))
        if not artist:
            continue
        counts[artist] = counts.get(artist, 0) + 1

    if not counts:
        return "", 0

    items = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return items[0]


def search_songs(songs: List[Song], query: str, field: str = "artist") -> List[Song]:
    """
    Return songs matching the query on a given field.

    Intended rule:
    - case-insensitive
    - partial match: query must be contained within the song's field value

    Fix: The starter code accidentally checked `value in q` (backwards),
    which breaks partial search like "AC" -> "AC/DC".
    """
    if not query:
        return songs

    q = str(query).lower().strip()
    filtered: List[Song] = []

    for song in songs:
        value = str(song.get(field, "") or "").lower()
        if value and q in value:
            filtered.append(song)

    return filtered


def lucky_pick(playlists: PlaylistMap, mode: str = "any") -> Optional[Song]:
    """
    Pick a song from the playlists according to mode.

    Intended rule:
    - "hype" => pick only from Hype
    - "chill" => pick only from Chill
    - "any" => pick from the combined pool (Hype + Chill + ideally Mixed)
    """
    mode = (mode or "any").lower().strip()

    if mode == "hype":
        songs = playlists.get("Hype", [])
    elif mode == "chill":
        songs = playlists.get("Chill", [])
    else:
        songs = playlists.get("Hype", []) + playlists.get("Chill", []) + playlists.get("Mixed", [])

    return random_choice_or_none(songs)


def random_choice_or_none(songs: List[Song]) -> Optional[Song]:
    """
    Return a random song or None.

    Fix: `random.choice([])` crashes, so I guard against empty input.
    """
    import random

    if not songs:
        return None
    return random.choice(songs)


def history_summary(history: List[Song]) -> Dict[str, int]:
    """Return a summary of moods seen in the history (safe for unknown mood values)."""
    counts = {"Hype": 0, "Chill": 0, "Mixed": 0}
    for song in history:
        mood = str(song.get("mood", "Mixed") or "Mixed")
        if mood not in counts:
            counts["Mixed"] += 1
        else:
            counts[mood] += 1
    return counts
