"""
email_generator.py - Core Email Generation Engine.

Implements the Strategy Pattern with two prompt strategies:
  - AdvancedStrategy: Role-Playing + Few-Shot + Chain-of-Thought
  - BasicStrategy: Zero-Shot Direct Prompting

Uses the native OpenAI SDK for full control over prompt formatting.
"""

import re
import logging
from config import (
    client,
    GENERATION_MODEL,
    ADVANCED_SYSTEM_PROMPT,
    ADVANCED_USER_PROMPT_TEMPLATE,
    BASIC_SYSTEM_PROMPT,
    BASIC_USER_PROMPT_TEMPLATE,
)

logger = logging.getLogger(__name__)


def _format_key_facts(key_facts: list[str]) -> str:
    """Format a list of key facts into a bulleted string for prompt insertion."""
    return "\n".join(f"  - {fact}" for fact in key_facts)


def _extract_thinking_and_email(raw_output: str) -> dict:
    """
    Parse the model output to separate the <thinking> block from the final email.
    Returns a dict with 'thinking' (str or None) and 'email' (str).
    """
    thinking_match = re.search(
        r"<thinking>(.*?)</thinking>", raw_output, re.DOTALL
    )
    thinking = thinking_match.group(1).strip() if thinking_match else None

    # Remove the thinking block to isolate the email
    email = re.sub(
        r"<thinking>.*?</thinking>", "", raw_output, flags=re.DOTALL
    ).strip()

    return {"thinking": thinking, "email": email}


def generate_email(
    intent: str,
    key_facts: list[str],
    tone: str,
    strategy: str = "advanced",
) -> dict:
    """
    Generate a professional email using the specified prompting strategy.

    Args:
        intent: The core purpose of the email.
        key_facts: List of facts to include in the email.
        tone: The desired writing style.
        strategy: 'advanced' (Few-Shot + CoT + Role-Play) or 'basic' (Zero-Shot).

    Returns:
        dict with keys:
            - 'email': The generated email text.
            - 'thinking': Chain-of-thought trace (None for basic strategy).
            - 'strategy': The strategy name used.
    """
    key_facts_formatted = _format_key_facts(key_facts)

    if strategy == "advanced":
        system_prompt = ADVANCED_SYSTEM_PROMPT
        user_prompt = ADVANCED_USER_PROMPT_TEMPLATE.format(
            intent=intent,
            key_facts_formatted=key_facts_formatted,
            tone=tone,
        )
    elif strategy == "basic":
        system_prompt = BASIC_SYSTEM_PROMPT
        user_prompt = BASIC_USER_PROMPT_TEMPLATE.format(
            intent=intent,
            key_facts_formatted=key_facts_formatted,
            tone=tone,
        )
    else:
        raise ValueError(f"Unknown strategy: '{strategy}'. Use 'advanced' or 'basic'.")

    logger.info(f"Generating email with strategy='{strategy}', model='{GENERATION_MODEL}'")

    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=1500,
    )

    raw_output = response.choices[0].message.content.strip()

    # Parse thinking block for advanced strategy
    if strategy == "advanced":
        parsed = _extract_thinking_and_email(raw_output)
    else:
        parsed = {"thinking": None, "email": raw_output}

    parsed["strategy"] = strategy
    return parsed
