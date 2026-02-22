import os
import sys
import json

from test_runner import run_tests
from scorer import compute_score
from static_analysis import run_static_analysis
from complexity_detector import detect_complexity
from llm_feedback import generate_llm_feedback
from meta_evaluator import (
    compute_uncertainty_flags,
    consistency_check,
    hallucination_check
)

PROBLEMS_DIR = "problems"


def detect_problem(submission_path):
    with open(submission_path, "r") as f:
        code = f.read()

    if "def two_sum" in code:
        return "two_sum"
    elif "def fib" in code:
        return "fib"
    elif "def climb_stairs" in code:
        return "climb_stairs"
    elif "def is_valid" in code:
        return "is_valid"
    elif "def count_components" in code:
        return "count_components"
    else:
        return None


def generate_report(problem_name, submission_path):
    problem_dir = os.path.join(PROBLEMS_DIR, problem_name)

    test_results = run_tests(problem_dir, submission_path)

    if "structural_error" in test_results:
        return test_results

    static_results = run_static_analysis(submission_path)
    complexity_results = detect_complexity(submission_path)
    score = compute_score(test_results, static_results, complexity_results)

    with open(os.path.join(problem_dir, "problem_statement.txt")) as f:
        problem_statement = f.read()

    with open(submission_path) as f:
        submission_code = f.read()

    llm_output = generate_llm_feedback(
        problem_statement,
        submission_code,
        test_results,
        static_results,
        complexity_results
    )

    uncertainty_flags = compute_uncertainty_flags(
        test_results,
        complexity_results
    )

    is_consistent = consistency_check(
        problem_dir,
        submission_path,
        run_tests,
        run_static_analysis,
        detect_complexity,
        compute_score
    )

    hallucinations = hallucination_check(
        llm_output,
        test_results
    )

    return {
        "problem": problem_name,
        "score": score["total_score"],
        "score_breakdown": score,
        "test_summary": f"{test_results['passed']} / {test_results['total']} tests passed",
        "llm_feedback": llm_output,
        "uncertainty_flags": uncertainty_flags,
        "consistent": is_consistent,
        "hallucination_flags": hallucinations
    }


def print_clean_report(report):
    print("\n" + "=" * 60)
    print("🧠 AI CODE EVALUATION REPORT")
    print("=" * 60)

    if "structural_error" in report:
        print("❌ Structural Error:")
        print(report["structural_error"])
        return

    print(f"\n📘 Problem: {report['problem']}")
    print(f"🎯 Final Score: {report['score']} / 10")
    print(f"✅ Tests: {report['test_summary']}")

    print("\n📊 Score Breakdown:")
    for k, v in report["score_breakdown"].items():
        print(f"   {k.replace('_', ' ').title()}: {v}")

    feedback = report["llm_feedback"]

    print("\n📝 LLM Feedback:")
    if feedback.get("issues"):
        print("  🔴 Issues:")
        for issue in feedback["issues"]:
            print(f"   - {issue}")
    else:
        print("  🔴 Issues: None")

    if feedback.get("suggestions"):
        print("  💡 Suggestions:")
        for sug in feedback["suggestions"]:
            print(f"   - {sug}")
    else:
        print("  💡 Suggestions: None")

    if feedback.get("complexity_comment"):
        print(f"  ⚙ Complexity: {feedback['complexity_comment']}")

    print(f"\n🔎 Confidence: {feedback.get('confidence', 0)}")

    print("\n⚠ Uncertainty Flags:")
    if report["uncertainty_flags"]:
        for flag in report["uncertainty_flags"]:
            print(f"   - {flag}")
    else:
        print("   None")

    print(f"\n🔁 Consistency Check: {'PASS' if report['consistent'] else 'FAIL'}")

    print("\n🧠 Hallucination Audit:")
    if report["hallucination_flags"]:
        for h in report["hallucination_flags"]:
            print(f"   - {h}")
    else:
        print("   None detected")

    print("=" * 60)


if __name__ == "__main__":
    submission_path = sys.argv[1]

    problem = detect_problem(submission_path)

    if not problem:
        print("❌ Could not detect problem type.")
        sys.exit(1)

    report = generate_report(problem, submission_path)

    print_clean_report(report)

    output_file = submission_path.replace(".py", "_report.json")
    with open(output_file, "w") as f:
        json.dump(report, f, indent=4)

    print(f"\n📄 Report saved as: {output_file}")