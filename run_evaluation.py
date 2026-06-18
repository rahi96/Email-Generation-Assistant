"""
run_evaluation.py - CLI Evaluation Runner for the Email Generation Assistant.

Runs all 10 test scenarios through both prompting strategies (Advanced & Basic),
evaluates each generated email using 3 custom metrics, and outputs:
  - evaluation_results.json (full detailed report)
  - evaluation_results.csv (summary table)
  - Console summary with averages
"""

import json
import logging
import sys
from datetime import datetime

import pandas as pd

from email_generator import generate_email
from evaluation_metrics import (
    evaluate_fact_recall,
    evaluate_tone_adherence,
    evaluate_format_adherence,
)
from evaluation_scenarios import SCENARIOS

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("EvaluationRunner")

STRATEGIES = ["advanced", "basic"]


def run_single_scenario(scenario: dict, strategy: str) -> dict:
    """Generate an email and evaluate it for a single scenario + strategy."""
    logger.info(
        f"  → Scenario {scenario['id']} | Strategy: {strategy} | "
        f"Tone: {scenario['tone']}"
    )

    # Step 1: Generate email
    gen_result = generate_email(
        intent=scenario["intent"],
        key_facts=scenario["key_facts"],
        tone=scenario["tone"],
        strategy=strategy,
    )

    generated_email = gen_result["email"]
    thinking = gen_result.get("thinking")

    # Step 2: Evaluate with all 3 metrics
    fact_recall = evaluate_fact_recall(generated_email, scenario["key_facts"])
    tone_adherence = evaluate_tone_adherence(generated_email, scenario["tone"])
    format_adherence = evaluate_format_adherence(generated_email)

    return {
        "generated_email": generated_email,
        "thinking": thinking,
        "scores": {
            "fact_recall": fact_recall["score"],
            "tone_adherence": tone_adherence["score"],
            "format_adherence": format_adherence["score"],
        },
        "metric_details": {
            "fact_recall": fact_recall,
            "tone_adherence": tone_adherence,
            "format_adherence": format_adherence,
        },
    }


def run_full_evaluation() -> dict:
    """
    Execute the full evaluation pipeline across all scenarios and strategies.

    Returns:
        dict containing all results, metric definitions, and averages.
    """
    logger.info("=" * 70)
    logger.info("STARTING FULL EVALUATION RUN")
    logger.info(f"Scenarios: {len(SCENARIOS)} | Strategies: {STRATEGIES}")
    logger.info("=" * 70)

    results = {
        "metadata": {
            "run_timestamp": datetime.now().isoformat(),
            "num_scenarios": len(SCENARIOS),
            "strategies": STRATEGIES,
        },
        "metrics_definitions": {
            "fact_recall": {
                "name": "Fact Recall & Integration Accuracy",
                "description": (
                    "Measures the percentage of input Key Facts that are "
                    "semantically present in the generated email using "
                    "LLM-as-a-Judge evaluation."
                ),
                "score_range": "0.0 to 1.0",
                "methodology": "LLM-as-a-Judge (semantic matching)",
            },
            "tone_adherence": {
                "name": "Tone Adherence Score",
                "description": (
                    "Evaluates whether the vocabulary, pacing, and overall "
                    "style of the email align with the specified target tone."
                ),
                "score_range": "1 to 5",
                "methodology": "LLM-as-a-Judge (tone analysis)",
            },
            "format_adherence": {
                "name": "Structural Professionalism & Formatting",
                "description": (
                    "Evaluates email structure (Subject, Greeting, Sign-off) "
                    "and checks for template placeholders. Combines programmatic "
                    "rule checks (50%) with LLM-as-a-Judge assessment (50%)."
                ),
                "score_range": "1 to 5",
                "methodology": "Hybrid: Programmatic regex checks + LLM-as-a-Judge",
            },
        },
        "scenarios": [],
        "overall_averages": {},
    }

    # Accumulators for averages
    score_accumulators = {
        strategy: {"fact_recall": [], "tone_adherence": [], "format_adherence": []}
        for strategy in STRATEGIES
    }

    for scenario in SCENARIOS:
        logger.info(f"\n{'─' * 50}")
        logger.info(f"SCENARIO {scenario['id']}: {scenario['intent'][:60]}...")

        scenario_result = {
            "id": scenario["id"],
            "intent": scenario["intent"],
            "key_facts": scenario["key_facts"],
            "tone": scenario["tone"],
            "human_reference": scenario["human_reference"],
            "results": {},
        }

        for strategy in STRATEGIES:
            result = run_single_scenario(scenario, strategy)
            scenario_result["results"][strategy] = result

            # Accumulate scores
            for metric_name, score in result["scores"].items():
                score_accumulators[strategy][metric_name].append(score)

        results["scenarios"].append(scenario_result)

    # Calculate averages
    for strategy in STRATEGIES:
        averages = {}
        for metric_name, scores in score_accumulators[strategy].items():
            averages[metric_name] = round(sum(scores) / len(scores), 3) if scores else 0
        results["overall_averages"][strategy] = averages

    return results


def save_json_report(results: dict, filepath: str = "evaluation_results.json"):
    """Save the full evaluation results to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info(f"JSON report saved to: {filepath}")


def save_csv_report(results: dict, filepath: str = "evaluation_results.csv"):
    """Save a summary CSV table with per-scenario, per-strategy scores."""
    rows = []
    for scenario in results["scenarios"]:
        for strategy, result in scenario["results"].items():
            rows.append(
                {
                    "Scenario_ID": scenario["id"],
                    "Intent": scenario["intent"][:80],
                    "Tone": scenario["tone"],
                    "Strategy": strategy,
                    "Fact_Recall": result["scores"]["fact_recall"],
                    "Tone_Adherence": result["scores"]["tone_adherence"],
                    "Format_Adherence": result["scores"]["format_adherence"],
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)
    logger.info(f"CSV report saved to: {filepath}")


def print_summary(results: dict):
    """Print a formatted summary table to the console."""
    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    for strategy in STRATEGIES:
        avgs = results["overall_averages"][strategy]
        print(f"\n{'─' * 40}")
        print(f"  Strategy: {strategy.upper()}")
        print(f"{'─' * 40}")
        print(f"  Fact Recall (0-1):      {avgs['fact_recall']:.3f}")
        print(f"  Tone Adherence (1-5):   {avgs['tone_adherence']:.3f}")
        print(f"  Format Adherence (1-5): {avgs['format_adherence']:.3f}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    results = run_full_evaluation()
    save_json_report(results)
    save_csv_report(results)
    print_summary(results)
    logger.info("Evaluation run complete.")
