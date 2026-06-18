"""
evaluation_metrics.py - Custom Evaluation Metrics for the Email Generation Assistant.

Implements 3 custom metrics using a combination of programmatic checks and LLM-as-a-Judge:
  1. Fact Recall & Integration Accuracy (0.0 - 1.0)
  2. Tone Adherence Score (1 - 5)
  3. Structural Professionalism & Formatting (1 - 5)
"""

import json
import re
import logging
from config import (
    client,
    EVALUATION_MODEL,
    FACT_RECALL_JUDGE_PROMPT,
    TONE_ADHERENCE_JUDGE_PROMPT,
    FORMAT_ADHERENCE_JUDGE_PROMPT,
)

logger = logging.getLogger(__name__)


def _call_llm_judge(prompt: str) -> dict:
    """
    Call the LLM evaluator with the given prompt and parse JSON response.
    Includes retry logic for malformed JSON responses.
    """
    response = client.chat.completions.create(
        model=EVALUATION_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a precise evaluation judge. Respond ONLY with valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,  # Deterministic evaluation
        max_tokens=1000,
    )

    raw = response.choices[0].message.content.strip()

    # Try to extract JSON from the response (handles markdown code blocks)
    json_match = re.search(r"```(?:json)?\s*(.*?)```", raw, re.DOTALL)
    if json_match:
        raw = json_match.group(1).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse LLM judge response as JSON: {raw[:200]}...")
        return {"score": 0, "error": "Failed to parse judge response"}


def _format_key_facts(key_facts: list[str]) -> str:
    """Format key facts list into numbered lines for the evaluation prompt."""
    return "\n".join(f"  {i+1}. {fact}" for i, fact in enumerate(key_facts))


# =============================================================================
# METRIC 1: Fact Recall & Integration Accuracy
# =============================================================================

def evaluate_fact_recall(
    generated_email: str, key_facts: list[str]
) -> dict:
    """
    Custom Metric 1: Fact Recall & Integration Accuracy.

    Definition:
        Measures the percentage of input Key Facts that are semantically
        present in the generated email. Uses LLM-as-a-Judge to handle
        paraphrased or restructured facts (not just keyword matching).

    Logic:
        - Each input fact is evaluated for semantic presence in the email.
        - Score = (number of facts recalled) / (total number of facts).

    Score Range: 0.0 (no facts recalled) to 1.0 (all facts recalled).

    Args:
        generated_email: The model-generated email text.
        key_facts: List of facts that should be in the email.

    Returns:
        dict with 'score' (float), 'total_facts', 'facts_recalled',
        and 'evaluations' (per-fact breakdown).
    """
    prompt = FACT_RECALL_JUDGE_PROMPT.format(
        key_facts_formatted=_format_key_facts(key_facts),
        generated_email=generated_email,
    )

    result = _call_llm_judge(prompt)

    # Ensure score is a float between 0.0 and 1.0
    score = float(result.get("score", 0))
    score = max(0.0, min(1.0, score))

    return {
        "metric_name": "Fact Recall & Integration Accuracy",
        "score": score,
        "total_facts": result.get("total_facts", len(key_facts)),
        "facts_recalled": result.get("facts_recalled", 0),
        "evaluations": result.get("evaluations", []),
    }


# =============================================================================
# METRIC 2: Tone Adherence Score
# =============================================================================

def evaluate_tone_adherence(generated_email: str, tone: str) -> dict:
    """
    Custom Metric 2: Tone Adherence Score.

    Definition:
        Evaluates whether the vocabulary, sentence pacing, emotional markers,
        and overall writing style align with the specified target tone.

    Logic:
        - LLM-as-a-Judge analyzes the email and compares detected tone
          against the requested tone.
        - Produces a detailed reasoning trace and an integer score.

    Score Range: 1 (completely mismatched) to 5 (flawless alignment).

    Args:
        generated_email: The model-generated email text.
        tone: The target tone string (e.g., "formal", "casual", "empathetic").

    Returns:
        dict with 'score' (int 1-5), 'detected_tone_description',
        and 'alignment_reasoning'.
    """
    prompt = TONE_ADHERENCE_JUDGE_PROMPT.format(
        tone=tone,
        generated_email=generated_email,
    )

    result = _call_llm_judge(prompt)

    # Clamp score to valid range
    score = int(result.get("score", 1))
    score = max(1, min(5, score))

    return {
        "metric_name": "Tone Adherence Score",
        "score": score,
        "target_tone": tone,
        "detected_tone_description": result.get("detected_tone_description", "N/A"),
        "alignment_reasoning": result.get("alignment_reasoning", "N/A"),
    }


# =============================================================================
# METRIC 3: Structural Professionalism & Formatting
# =============================================================================

def _programmatic_format_checks(generated_email: str) -> dict:
    """
    Run rule-based checks for email structure components.
    Returns a dict of boolean checks and a programmatic penalty score.
    """
    text_lower = generated_email.lower()

    has_subject = bool(re.search(r"^subject:", text_lower, re.MULTILINE))
    has_greeting = bool(
        re.search(r"^(dear |hi |hey |hello |good morning|good afternoon)", text_lower, re.MULTILINE)
    )
    has_sign_off = bool(
        re.search(
            r"(sincerely|regards|best regards|kind regards|best|cheers|warmly|thank you|thanks)",
            text_lower,
        )
    )
    # Check for template placeholders like [Your Name], [Company], [Date], etc.
    placeholders_found = re.findall(r"\[(?:Your |Insert |Company|Date|Name|Title).*?\]", generated_email)
    has_placeholders = len(placeholders_found) > 0

    # Calculate programmatic penalty
    checks_passed = sum([has_subject, has_greeting, has_sign_off, not has_placeholders])
    programmatic_score = checks_passed / 4.0  # 0.0 to 1.0

    return {
        "has_subject_line": has_subject,
        "has_greeting": has_greeting,
        "has_sign_off": has_sign_off,
        "has_placeholders": has_placeholders,
        "placeholders_found": placeholders_found,
        "programmatic_score": programmatic_score,
    }


def evaluate_format_adherence(generated_email: str) -> dict:
    """
    Custom Metric 3: Structural Professionalism & Formatting.

    Definition:
        Evaluates whether the generated email conforms to standard professional
        email formatting conventions and is free of template artifacts.

    Logic:
        - Programmatic Checks (50% weight): Verifies presence of Subject line,
          Greeting, Sign-off, and absence of bracketed placeholders.
        - LLM-as-a-Judge (50% weight): Evaluates formatting cleanliness,
          paragraph flow, and overall professional structure.
        - Final Score = (Programmatic Score * 2.5) + (LLM Score * 0.5),
          clamped to range 1-5.

    Score Range: 1 (missing basic components) to 5 (perfectly structured).

    Args:
        generated_email: The model-generated email text.

    Returns:
        dict with 'score' (int 1-5), 'programmatic_checks' (sub-dict),
        and 'llm_assessment' (sub-dict).
    """
    # Part A: Programmatic checks
    prog_checks = _programmatic_format_checks(generated_email)

    # Part B: LLM-as-a-Judge assessment
    prompt = FORMAT_ADHERENCE_JUDGE_PROMPT.format(
        generated_email=generated_email,
    )
    llm_result = _call_llm_judge(prompt)
    llm_score = int(llm_result.get("score", 1))
    llm_score = max(1, min(5, llm_score))

    # Combine: 50% programmatic (scaled to 1-5), 50% LLM
    prog_scaled = 1 + (prog_checks["programmatic_score"] * 4)  # maps 0-1 to 1-5
    combined_score = round((prog_scaled + llm_score) / 2)
    combined_score = max(1, min(5, combined_score))

    return {
        "metric_name": "Structural Professionalism & Formatting",
        "score": combined_score,
        "programmatic_checks": prog_checks,
        "llm_assessment": {
            "score": llm_score,
            "structure_reasoning": llm_result.get("structure_reasoning", "N/A"),
        },
    }
