import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import torch
import json
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

logging.set_verbosity_error()

MODEL_NAME = "Qwen/Qwen2.5-Coder-3B-Instruct"

MODEL_NAME = "Qwen/Qwen2.5-Coder-3B-Instruct"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16,
    device_map="auto"
)

print("Model loaded successfully.")


def generate_llm_feedback(problem_statement,
                          submission_code,
                          test_results,
                          static_results,
                          complexity_results):

    system_prompt = """
You are an automated coding evaluator.

You MUST:
- Use only provided evidence.
- Not invent errors.
- Not modify numeric scores.
- Output STRICT JSON only.
- Do NOT include markdown formatting.
"""

    user_prompt = f"""
Return STRICT JSON in this exact format:

{{
  "issues": [],
  "suggestions": [],
  "conceptual_errors": [],
  "complexity_comment": "",
  "confidence": 0.0
}}

Problem:
{problem_statement}

Student Code:
{submission_code}

Test Results:
{json.dumps(test_results, indent=2)}

Static Analysis:
{json.dumps(static_results, indent=2)}

Complexity Analysis:
{json.dumps(complexity_results, indent=2)}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Apply Qwen chat template properly
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=400,
        do_sample=False  # deterministic
    )

    # Decode ONLY newly generated tokens
    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # Clean markdown fences if model still adds them
    response = response.strip()
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    # Extract JSON safely
    try:
        match = re.search(r"\{[\s\S]*\}", response)
        if match:
            json_output = match.group(0)
            return json.loads(json_output)
        else:
            raise ValueError("No JSON object found")

    except Exception:
        print("RAW CLEANED MODEL OUTPUT:\n", response)
        return {
            "issues": [],
            "suggestions": ["LLM output parsing failed"],
            "conceptual_errors": [],
            "complexity_comment": "",
            "confidence": 0.0
        }