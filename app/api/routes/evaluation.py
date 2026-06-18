"""
evaluation.py - FastAPI Route for running the Evaluation Pipeline.

Endpoint: POST /api/v1/evaluation/run
Triggers the full 10-scenario benchmark and returns structured results.
"""

import logging

from fastapi import APIRouter, HTTPException

from app.schemas.evaluation import (
    EvaluationResponse,
    MetricDefinition,
    MetricScores,
    ScenarioResult,
    StrategyResult,
)
from run_evaluation import run_full_evaluation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post(
    "/run",
    response_model=EvaluationResponse,
    summary="Run the full evaluation benchmark",
    description=(
        "Runs all 10 test scenarios through both prompting strategies "
        "(Advanced & Basic), evaluates each with 3 custom metrics, "
        "and returns the structured results with averages."
    ),
)
def run_evaluation_endpoint():
    """
    Execute the full evaluation pipeline.

    This endpoint runs all 10 scenarios, generates emails with both
    'advanced' and 'basic' strategies, evaluates each using 3 custom
    metrics, and returns the complete results including per-scenario
    scores and overall averages.

    **Note**: This may take several minutes due to multiple LLM API calls.
    """
    try:
        logger.info("Evaluation run triggered via API endpoint")
        results = run_full_evaluation()

        # Transform internal results dict into Pydantic response models
        metrics_definitions = {
            key: MetricDefinition(**val)
            for key, val in results["metrics_definitions"].items()
        }

        overall_averages = {
            strategy: MetricScores(**scores)
            for strategy, scores in results["overall_averages"].items()
        }

        scenarios_raw = []
        for scenario in results["scenarios"]:
            strategy_results = {}
            for strategy_name, result in scenario["results"].items():
                strategy_results[strategy_name] = StrategyResult(
                    email=result["generated_email"],
                    thinking=result.get("thinking"),
                    scores=MetricScores(**result["scores"]),
                )

            scenarios_raw.append(
                ScenarioResult(
                    id=scenario["id"],
                    intent=scenario["intent"],
                    tone=scenario["tone"],
                    key_facts=scenario["key_facts"],
                    results=strategy_results,
                )
            )

        return EvaluationResponse(
            status="success",
            metrics_definitions=metrics_definitions,
            overall_averages=overall_averages,
            scenarios_raw=scenarios_raw,
        )

    except Exception as e:
        logger.error(f"Evaluation run failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation run failed: {str(e)}",
        )
