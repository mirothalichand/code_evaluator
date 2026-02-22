import subprocess
import json

def run_static_analysis(submission_path):
    try:
        result = subprocess.run(
            ["ruff", submission_path, "--format", "json"],
            capture_output=True,
            text=True
        )

        issues = json.loads(result.stdout) if result.stdout else []

        return {
            "issue_count": len(issues),
            "issues": issues
        }

    except Exception as e:
        return {
            "issue_count": 0,
            "issues": [],
            "error": str(e)
        }