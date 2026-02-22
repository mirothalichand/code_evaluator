import os
import json
import statistics

from evaluate import generate_report, detect_problem

SUBMISSIONS_DIR = "submissions"


def load_gold_scores(gold_file):
    if not os.path.exists(gold_file):
        return {}

    with open(gold_file, "r") as f:
        return json.load(f)


def compute_dataset_metrics(results, gold_scores):
    predicted_scores = []
    gold_values = []

    for r in results:
        predicted_scores.append(r["score"])

        filename = r["file"]
        if filename in gold_scores:
            gold_values.append(gold_scores[filename])
        else:
            gold_values.append(None)

    # Remove None entries
    paired = [(p, g) for p, g in zip(predicted_scores, gold_values) if g is not None]

    if not paired:
        return {
            "mae": None,
            "agreement_rate": None
        }

    preds, golds = zip(*paired)

    # Mean Absolute Error
    mae = sum(abs(p - g) for p, g in paired) / len(paired)

    # Exact agreement
    agreement = sum(1 for p, g in paired if round(p, 2) == round(g, 2))
    agreement_rate = agreement / len(paired)

    return {
        "mae": round(mae, 3),
        "agreement_rate": round(agreement_rate, 3),
        "mean_score": round(statistics.mean(preds), 3),
        "std_score": round(statistics.stdev(preds), 3) if len(preds) > 1 else 0
    }


def batch_evaluate(submissions_dir, gold_file=None):
    gold_scores = load_gold_scores(gold_file) if gold_file else {}

    results = []

    for file in os.listdir(submissions_dir):
        if not file.endswith(".py"):
            continue

        file_path = os.path.join(submissions_dir, file)

        problem = detect_problem(file_path)
        if not problem:
            continue

        report = generate_report(problem, file_path)

        if "score" not in report:
            continue

        results.append({
            "file": file,
            "problem": problem,
            "score": report["score"]
        })

    metrics = compute_dataset_metrics(results, gold_scores)

    dataset_report = {
        "total_submissions": len(results),
        "results": results,
        "dataset_metrics": metrics
    }

    return dataset_report


if __name__ == "__main__":
    gold_file = "gold_scores.json"  # optional

    report = batch_evaluate(SUBMISSIONS_DIR, gold_file)

    print("\n" + "=" * 60)
    print("📊 DATASET EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total Submissions: {report['total_submissions']}")

    metrics = report["dataset_metrics"]

    if metrics["mae"] is not None:
        print(f"MAE: {metrics['mae']}")
        print(f"Agreement Rate: {metrics['agreement_rate']}")
        print(f"Mean Score: {metrics['mean_score']}")
        print(f"Std Dev: {metrics['std_score']}")
    else:
        print("No gold scores provided. Skipping accuracy metrics.")

    print("=" * 60)

    with open("dataset_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("📄 Dataset report saved as dataset_report.json")