"""
evaluation.py - Pydantic schemas for the Evaluation API.
"""

from pydantic import BaseModel, Field
from typing import Optional


class MetricScores(BaseModel):
    """Score container for a single evaluation."""

    fact_recall: float = Field(description="Fact Recall & Integration score (0.0-1.0)")
    tone_adherence: float = Field(description="Tone Adherence score (1-5)")
    format_adherence: float = Field(description="Structure & Formatting score (1-5)")


class StrategyResult(BaseModel):
    """Results for a single strategy on a single scenario."""

    email: str
    thinking: Optional[str] = None
    scores: MetricScores


class ScenarioResult(BaseModel):
    """Full evaluation result for a single scenario across strategies."""

    id: int
    intent: str
    tone: str
    key_facts: list[str]
    results: dict[str, StrategyResult]


class MetricDefinition(BaseModel):
    """Definition of a custom evaluation metric."""

    name: str
    description: str
    score_range: str
    methodology: str


class EvaluationResponse(BaseModel):
    """Response body from the evaluation run endpoint."""

    status: str = Field(default="success")
    metrics_definitions: dict[str, MetricDefinition]
    overall_averages: dict[str, MetricScores]
    scenarios_raw: list[ScenarioResult]
