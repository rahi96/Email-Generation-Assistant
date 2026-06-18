"""
email.py - FastAPI Route for Email Generation.

Endpoint: POST /api/v1/email/generate
Generates a professional email and logs the result to SQLite.
"""

import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.email_log import EmailLog
from app.schemas.email import EmailGenerateRequest, EmailGenerateResponse
from email_generator import generate_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["Email Generation"])


@router.post(
    "/generate",
    response_model=EmailGenerateResponse,
    summary="Generate a professional email",
    description=(
        "Takes intent, key facts, tone, and strategy as input. "
        "Returns a generated professional email and logs the result to the database."
    ),
)
def generate_email_endpoint(
    payload: EmailGenerateRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a professional email using the specified prompting strategy.

    - **intent**: The core purpose of the email
    - **key_facts**: List of facts to seamlessly include
    - **tone**: Writing style (e.g., formal, casual, urgent)
    - **strategy**: 'advanced' (Few-Shot + CoT) or 'basic' (Zero-Shot)
    """
    try:
        # Step 1: Generate the email
        result = generate_email(
            intent=payload.intent,
            key_facts=payload.key_facts,
            tone=payload.tone,
            strategy=payload.strategy,
        )

        # Step 2: Log to SQLite database
        db_log = EmailLog(
            intent=payload.intent,
            key_facts=json.dumps(payload.key_facts),
            tone=payload.tone,
            strategy=payload.strategy,
            generated_email=result["email"],
            thinking=result.get("thinking"),
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        logger.info(f"Email generated and logged (ID: {db_log.id})")

        # Step 3: Return response
        return EmailGenerateResponse(
            strategy_used=payload.strategy,
            generated_email=result["email"],
            thinking=result.get("thinking"),
            log_id=db_log.id,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Email generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
