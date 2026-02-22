
Use this professional version:

---

## DESIGN_NOTE.md (Paste This)

```markdown
# Design Note – AI Code Evaluation System

## 1. Overview

This system implements a hybrid automated grading pipeline combining deterministic evaluation with LLM-assisted reasoning. The design ensures reliability, explainability, and measurable grading performance.

The system evaluates 5 problem categories:
- Arrays/Strings
- Recursion
- DP-lite
- Parsing
- Graphs-lite

A total of 50 test cases are distributed across the problems, and 40 diverse submission variants are used for dataset evaluation.

---

## 2. System Architecture

The pipeline consists of:

1. Test Execution Layer  
   - Runs submission in isolated temporary directory  
   - Enforces timeout to prevent infinite loops  
   - Captures runtime errors  

2. Structural Validation  
   - Verifies required function exists  
   - Detects syntax errors  

3. Static Analysis  
   - Uses `ruff` to detect code quality issues  

4. Complexity Detection  
   - Counts loops and recursion usage  
   - Flags potential inefficiencies  

5. LLM Feedback Layer  
   - Uses Qwen open-source model  
   - Produces structured JSON feedback  
   - Identifies conceptual and performance issues  

6. Meta-Evaluation Layer  
   - Uncertainty flag detection  
   - Consistency checking  
   - Hallucination detection  

7. Dataset Evaluation  
   - Batch evaluation over all submissions  
   - Computes MAE and agreement rate against gold scores  

---

## 3. Reliability Mechanisms

- Sandboxed execution
- Timeout enforcement
- Deterministic test reruns
- Hallucination auditing
- JSON-only LLM parsing

---

## 4. Evaluation Metrics

Dataset-level metrics include:

- Mean Absolute Error (MAE)
- Agreement rate
- Mean predicted score
- Score standard deviation

These metrics allow objective comparison between automated grading and human gold scores.

---

## 5. Design Trade-offs

The system balances:
- Deterministic correctness (unit tests)
- Reasoning-based feedback (LLM)
- Safety and reproducibility

LLM output does not directly modify numeric score. It enhances qualitative feedback while preserving deterministic scoring integrity.

---

## 6. Conclusion

This design demonstrates a robust, explainable, and scalable AI-assisted grading pipeline aligned with the assignment requirements.