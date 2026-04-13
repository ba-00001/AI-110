from .evaluation import print_evaluation_summary
from .system import MusicIntelligenceSystem


DEMO_PROFILES = [
    {
        "label": "Happy pop workout",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    },
    {
        "label": "Chill study session",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},
    },
    {
        "label": "Unknown genre stress test",
        "prefs": {"genre": "reggaeton", "mood": "focused", "energy": 1.2, "likes_acoustic": False},
    },
]


def main() -> None:
    system = MusicIntelligenceSystem()

    print("\nApplied AI Music Intelligence System")
    print("====================================")

    for profile in DEMO_PROFILES:
        result = system.run(profile["prefs"], k=3)
        print(f"\nScenario: {profile['label']}")
        print(f"Request: {result['request']}")
        print(f"Overall confidence: {result['overall_confidence']:.2f}")

        if result["warnings"]:
            print("Warnings:")
            for warning in result["warnings"]:
                print(f"- {warning}")

        print("Retrieved context:")
        for item in result["retrieved_context"]:
            print(f"- {item['source']}: {item['snippet']}")

        print("Recommendations:")
        for rec in result["recommendations"]:
            print(f"- {rec['title']} by {rec['artist']} | score={rec['score']:.2f} | confidence={rec['confidence']:.2f}")
            print(f"  Why: {rec['explanation']}")

    print()
    print_evaluation_summary()


if __name__ == "__main__":
    main()
