"""
Entry point for the Mood Machine rule based mood analyzer.
"""

from typing import List

from dataset import SAMPLE_POSTS, TRUE_LABELS
from mood_analyzer import MoodAnalyzer


def evaluate_rule_based(posts: List[str], labels: List[str]) -> float:
    """
    Evaluate the rule based MoodAnalyzer on a labeled dataset.
    """
    analyzer = MoodAnalyzer()
    correct = 0
    total = len(posts)

    print("=== Rule Based Evaluation on SAMPLE_POSTS ===")
    for text, true_label in zip(posts, labels):
        predicted_label = analyzer.predict_label(text)
        reason = analyzer.explain(text)
        is_correct = predicted_label == true_label
        if is_correct:
            correct += 1

        print(
            f'"{text}" -> predicted={predicted_label}, true={true_label}\n'
            f"  {reason}"
        )

    if total == 0:
        print("\nNo labeled examples to evaluate.")
        return 0.0

    accuracy = correct / total
    print(f"\nRule based accuracy on SAMPLE_POSTS: {accuracy:.2f}")
    return accuracy


def run_batch_demo() -> None:
    """
    Run the MoodAnalyzer on the sample posts and print predictions only.
    """
    analyzer = MoodAnalyzer()
    print("\n=== Batch Demo on SAMPLE_POSTS (rule based) ===")
    for text in SAMPLE_POSTS:
        label = analyzer.predict_label(text)
        reason = analyzer.explain(text)
        print(f'"{text}" -> {label}\n  {reason}')


def run_breaker_demo() -> None:
    """
    Stress test the analyzer with hand-picked edge cases.
    """
    analyzer = MoodAnalyzer()
    breakers = [
        "I love getting stuck in traffic",
        "This dinner is fire",
        "I'm not sad, just tired",
        "I'm fine :) but also nervous",
    ]

    print("\n=== Breaker Sentences ===")
    for text in breakers:
        print(f'"{text}" -> {analyzer.predict_label(text)}')
        print(f"  {analyzer.explain(text)}")


def run_interactive_loop() -> None:
    """
    Let the user type sentences and see the predicted mood.
    """
    analyzer = MoodAnalyzer()
    print("\n=== Interactive Mood Machine (rule based) ===")
    print("Type a sentence to analyze its mood.")
    print("Type 'quit' or press Enter on an empty line to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input == "" or user_input.lower() == "quit":
            print("Goodbye from the Mood Machine.")
            break

        label = analyzer.predict_label(user_input)
        reason = analyzer.explain(user_input)
        print(f"Model: {label}")
        print(f"Why: {reason}")


if __name__ == "__main__":
    evaluate_rule_based(SAMPLE_POSTS, TRUE_LABELS)
    run_batch_demo()
    run_breaker_demo()
    run_interactive_loop()

    print("\nTip: After you explore the rule based model here,")
    print("run `python ml_experiments.py` to compare the ML model trained")
    print("on the same SAMPLE_POSTS and TRUE_LABELS.")
