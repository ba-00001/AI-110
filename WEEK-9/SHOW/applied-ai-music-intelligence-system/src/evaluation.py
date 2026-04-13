from typing import Dict, List

from .system import MusicIntelligenceSystem


EVALUATION_CASES: List[Dict] = [
    {
        "name": "happy pop drive",
        "input": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
        "expected_top_title": "Sunrise City",
        "minimum_confidence": 0.75,
    },
    {
        "name": "quiet study session",
        "input": {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},
        "expected_top_title": "Library Rain",
        "minimum_confidence": 0.75,
    },
    {
        "name": "focused coding block",
        "input": {"genre": "lofi", "mood": "focused", "energy": 0.4, "likes_acoustic": True},
        "expected_top_title": "Focus Flow",
        "minimum_confidence": 0.75,
    },
]


def run_evaluation() -> Dict:
    system = MusicIntelligenceSystem()
    results: List[Dict] = []

    for case in EVALUATION_CASES:
        output = system.run(case["input"], k=3)
        top_recommendation = output["recommendations"][0]
        passed = (
            top_recommendation["title"] == case["expected_top_title"]
            and output["overall_confidence"] >= case["minimum_confidence"]
        )

        results.append(
            {
                "name": case["name"],
                "passed": passed,
                "expected_top_title": case["expected_top_title"],
                "actual_top_title": top_recommendation["title"],
                "overall_confidence": output["overall_confidence"],
            }
        )

    passed_count = sum(1 for item in results if item["passed"])
    average_confidence = round(
        sum(item["overall_confidence"] for item in results) / len(results),
        2,
    )

    return {
        "cases": results,
        "passed": passed_count,
        "total": len(results),
        "average_confidence": average_confidence,
    }


def print_evaluation_summary() -> None:
    summary = run_evaluation()
    print("Evaluation Summary")
    print("==================")
    for case in summary["cases"]:
        status = "PASS" if case["passed"] else "FAIL"
        print(
            f"{status} | {case['name']} | expected={case['expected_top_title']} | "
            f"actual={case['actual_top_title']} | confidence={case['overall_confidence']:.2f}"
        )

    print()
    print(
        f"Passed {summary['passed']} of {summary['total']} cases. "
        f"Average confidence: {summary['average_confidence']:.2f}"
    )
