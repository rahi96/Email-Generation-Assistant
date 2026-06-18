"""
email.py - Pydantic schemas for the Email Generation API.
"""

from pydantic import BaseModel, Field
from typing import Optional


class EmailGenerateRequest(BaseModel):
    """Request body for the email generation endpoint."""

    intent: str = Field(
        ...,
        description="The core purpose of the email.",
        examples=["Follow up after meeting", "Request for proposal details"],
    )
    key_facts: list[str] = Field(
        ...,
        description="Bullet points of information that must be included in the email.",
        examples=[["Met on Tuesday", "Offered 10% discount", "Demo call next week"]],
    )
    tone: str = Field(
        ...,
        description="The desired writing style of the email.",
        examples=["formal", "casual", "urgent", "empathetic"],
    )
    strategy: str = Field(
        default="advanced",
        description="Prompting strategy: 'advanced' (Few-Shot + CoT + Role-Play) or 'basic' (Zero-Shot).",
        examples=["advanced", "basic"],
    )


class EmailGenerateResponse(BaseModel):
    """Response body from the email generation endpoint."""

    strategy_used: str = Field(description="The prompting strategy that was used.")
    generated_email: str = Field(description="The generated professional email.")
    thinking: Optional[str] = Field(
        default=None,
        description="Chain-of-Thought trace (only present for 'advanced' strategy).",
    )
    log_id: int = Field(description="Database log ID for this generation.")
