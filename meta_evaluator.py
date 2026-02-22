# meta_evaluator.py

def compute_uncertainty_flags(test_results, complexity_results):
    flags = []

    total_tests = test_results.get("total", 0)

    # Low coverage
    if total_tests < 5:
        flags.append("Low test coverage")

    # Edge-case detection (based on test names)
    edge_keywords = ["zero", "empty", "negative", "single", "one"]
    edge_tests_present = any(
        any(keyword in d.get("name", "") for keyword in edge_keywords)
        for d in test_results.get("details", [])
    )

    if not edge_tests_present:
        flags.append("Edge-case coverage uncertain")

    # Complexity not stress-tested
    if complexity_results.get("loop_count", 0) > 0 and not complexity_results.get("flags"):
        flags.append("Complexity not stress-tested")

    return flags


def consistency_check(problem_dir, submission_path,
                      run_tests_fn, static_fn,
                      complexity_fn, score_fn):

    first_test = run_tests_fn(problem_dir, submission_path)
    second_test = run_tests_fn(problem_dir, submission_path)

    if first_test != second_test:
        return False

    return True


def hallucination_check(llm_feedback, test_results):
    hallucinations = []

    # If LLM reports issues but no failed tests
    if test_results.get("failed", 0) == 0 and llm_feedback.get("issues"):
        hallucinations.append(
            "LLM reported issues despite all tests passing"
        )

    # Runtime hallucination
    runtime_issue = any(
        d.get("error_type") in ["timeout", "runtime_error", "exception"]
        for d in test_results.get("details", [])
    )

    if not runtime_issue:
        for issue in llm_feedback.get("issues", []):
            if isinstance(issue, str) and "runtime" in issue.lower():
                hallucinations.append(
                    "LLM claimed runtime issue without evidence"
                )

    return hallucinations