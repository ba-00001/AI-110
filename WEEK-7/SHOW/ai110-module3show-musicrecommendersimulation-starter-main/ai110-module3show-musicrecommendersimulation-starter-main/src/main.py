"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nMusic Recommender Simulation")
    print("============================")
    print(f"Profile: {user_prefs}\n")
    print("Top recommendations:\n")

    for song, score, explanation in recommendations:
        print(f"{song['title']} by {song['artist']}")
        print(f"Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
