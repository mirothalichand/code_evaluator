def compute_score(test_results, static_results, complexity_results):
    total_tests = test_results["total"]
    passed = test_results["passed"]

    # Correctness (7 pts)
    correctness_score = (passed / total_tests) * 7 if total_tests else 0

    # Edge cases (2 pts)
    edge_keywords = ["zero", "empty", "negative", "single", "one"]
    edge_failures = 0

    for d in test_results["details"]:
        if any(k in d["name"] for k in edge_keywords):
            edge_failures += 1

    if edge_failures == 0:
        edge_score = 2
    elif edge_failures == 1:
        edge_score = 1
    else:
        edge_score = 0

    # Runtime stability (1 pt)
    runtime_issue = any(
        d.get("error_type") in ["timeout", "runtime_error", "exception"]
        for d in test_results["details"]
    )
    runtime_score = 0 if runtime_issue else 1

    # Static penalty (max -1)
    static_penalty = min(static_results["issue_count"] * 0.1, 1)

    # Complexity penalty (max -1)
    complexity_penalty = 1 if "nested_loops_detected" in complexity_results["flags"] else 0

    total_score = correctness_score + edge_score + runtime_score
    total_score -= static_penalty
    total_score -= complexity_penalty

    return {
        "correctness_score": round(correctness_score, 2),
        "edge_score": edge_score,
        "runtime_score": runtime_score,
        "static_penalty": round(static_penalty, 2),
        "complexity_penalty": complexity_penalty,
        "total_score": round(max(total_score, 0), 2)
    }