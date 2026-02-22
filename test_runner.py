import subprocess
import json
import os
import sys
import tempfile
import shutil
import importlib.util

from scorer import compute_score
from static_analysis import run_static_analysis
from complexity_detector import detect_complexity
from llm_feedback import generate_llm_feedback

TIMEOUT_SECONDS = 3


# -------------------------------------------------
# FUNCTION MAP FOR 5 FINAL PROBLEMS
# -------------------------------------------------

function_map = {
    "two_sum": "two_sum",
    "fib": "fib",
    "climb_stairs": "climb_stairs",
    "is_valid": "is_valid",
    "count_components": "count_components"
}


def check_function_exists(problem_dir, submission_path):
    problem_name = os.path.basename(problem_dir)
    func_name = function_map.get(problem_name)

    try:
        spec = importlib.util.spec_from_file_location("student", submission_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        return False, "syntax_error", str(e)

    if not hasattr(module, func_name):
        return False, "missing_function", f"{func_name} not defined"

    return True, None, None


def run_single_test(problem_dir, submission_path, test_case):
    problem_name = os.path.basename(problem_dir)
    func_name = function_map.get(problem_name)

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_script = os.path.join(tmpdir, "runner.py")
        shutil.copy(submission_path, os.path.join(tmpdir, "student.py"))

        with open(temp_script, "w") as f:
            f.write(f"""
import json
from student import {func_name}

try:
    result = {func_name}(*{test_case["input"]})
    print(json.dumps({{"result": result}}))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
""")

        try:
            completed = subprocess.run(
                ["python", temp_script],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                cwd=tmpdir
            )

            if completed.returncode != 0:
                return {"status": "runtime_error", "error": completed.stderr.strip()}

            output = completed.stdout.strip()
            parsed = json.loads(output)

            if "error" in parsed:
                return {"status": "exception", "error": parsed["error"]}

            return {"status": "success", "result": parsed["result"]}

        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Execution timed out"}


def compare_results(problem_name, actual, expected):
    # Handle tuple vs list
    if isinstance(actual, tuple):
        actual = list(actual)

    # Special handling for two_sum (order doesn't matter)
    if problem_name == "two_sum":
        return sorted(actual) == sorted(expected)

    return actual == expected


def run_tests(problem_dir, submission_path):
    exists, error_type, error_msg = check_function_exists(problem_dir, submission_path)

    if not exists:
        return {
            "structural_error": {
                "type": error_type,
                "message": error_msg
            }
        }

    problem_name = os.path.basename(problem_dir)

    tests_path = os.path.join(problem_dir, "tests.json")

    with open(tests_path, "r") as f:
        tests = json.load(f)

    passed = 0
    failed = 0
    details = []

    for test in tests:
        result = run_single_test(problem_dir, submission_path, test)

        if result["status"] == "success":
            actual = result["result"]
            expected = test["expected"]

            if compare_results(problem_name, actual, expected):
                passed += 1
            else:
                failed += 1
                details.append({
                    "name": test["name"],
                    "expected": expected,
                    "actual": actual
                })
        else:
            failed += 1
            details.append({
                "name": test["name"],
                "expected": test["expected"],
                "error_type": result["status"],
                "error": result.get("error", "")
            })

    return {
        "passed": passed,
        "failed": failed,
        "total": len(tests),
        "details": details
    }