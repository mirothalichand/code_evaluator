# AI Code Evaluation System

This project implements an automated AI-assisted code evaluation pipeline supporting:

- Deterministic test execution
- Static analysis
- Complexity detection
- LLM-based reasoning feedback
- Uncertainty flags
- Hallucination detection
- Consistency checking
- Dataset-level evaluation metrics

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <PRIVATE_REPO_URL>
cd code_evaluator
```

### 2. Install dependencies
```
pip install -r requirements.txt
```
- Run Single Submission

```
python evaluate.py submissions/fib_1.py
```
- Run Dataset Evaluation
```
python dataset_evaluator.py
```
This will:

1. Evaluate all submissions in /submissions
2. Compute MAE and agreement rate
3. Save dataset_report.json

## Problem Categories

The system evaluates 5 problems:

1. Arrays/Strings: Two Sum
2. Recursion: Fibonacci
3. DP-lite: Climbing Stairs
4. Parsing: Valid Parentheses
5. Graphs-lite: Connected Components

Each problem contains 5-10 tests.

## Evaluation Features

- Unit test execution (sandboxed + timeout)
- Static analysis (ruff)
- Complexity detection
- LLM feedback (Qwen open-source model)
- Uncertainty flags
- Hallucination detection
- Deterministic consistency check
- Dataset-level grading accuracy metrics

## Dataset Metrics
- Mean Absolute Error (MAE)
- Agreement rate
- Mean score
- Standard deviation




