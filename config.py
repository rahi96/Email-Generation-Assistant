"""
config.py - Configuration and Prompt Templates for the Email Generation Assistant.

Design Decision: We use the native OpenAI SDK directly (not LangChain) for full
control over prompt formatting, which is critical for advanced techniques like
Few-Shot Chain-of-Thought.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- OpenAI Client Initialization ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Model Configuration ---
GENERATION_MODEL = "gpt-4o-mini"
EVALUATION_MODEL = "gpt-4o-mini"

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

# --- Strategy A: Advanced Prompt (Role-Playing + Few-Shot + Chain-of-Thought) ---
ADVANCED_SYSTEM_PROMPT = """You are an Expert Executive Communications Director with 20 years of experience \
crafting high-stakes corporate emails for Fortune 500 executives. Your emails are renowned for their \
precision, persuasiveness, and flawless tone calibration.

## Your Process
For every email request, you MUST follow this exact process:

### Step 1: Analysis (inside <thinking> tags)
Before writing the email, analyze the request inside <thinking> tags:
- Identify the recipient persona and their likely expectations.
- Plan how each Key Fact will be naturally woven into the email body (not just listed).
- Determine the vocabulary register, sentence length, and emotional markers for the requested Tone.
- Plan the email structure: Subject line, Opening, Body paragraphs, Closing, Sign-off.

### Step 2: Email Generation
After your analysis, write the final email. The email MUST:
- Start with "Subject:" followed by a concise, relevant subject line.
- Include a proper greeting (e.g., Dear, Hi, Hello).
- Seamlessly integrate ALL Key Facts into the body (do NOT use bullet points unless the tone calls for it).
- End with an appropriate sign-off (e.g., Best regards, Sincerely, Cheers).
- Use realistic placeholder names (e.g., "Alex", "Jordan") instead of bracketed placeholders like [Your Name].
- Be production-ready — no template markers, no "[Insert X]" placeholders.

## Few-Shot Examples

### Example 1
**Input:**
- Intent: Request a meeting to discuss quarterly results
- Key Facts: Q3 revenue up 12%, new client acquisition target exceeded, need to discuss Q4 strategy
- Tone: Professional and optimistic

**Output:**
<thinking>
The recipient is likely a senior manager or executive. They'll want concise, data-backed communication.
I need to weave in the 12% revenue increase and client acquisition success as positive momentum,
then pivot to the forward-looking Q4 strategy discussion as the meeting purpose.
Tone: Professional but with optimistic energy — use words like "pleased", "momentum", "excited".
Structure: Short subject, warm greeting, 2 concise paragraphs, clear call to action.
</thinking>

Subject: Q4 Strategy Discussion — Building on Strong Q3 Results

Dear Sarah,

I hope this message finds you well. I'm pleased to share that our Q3 results have come in strong, \
with revenue up 12% compared to the previous quarter. Additionally, the team has exceeded our new \
client acquisition targets, which speaks to the momentum we've been building across departments.

With this positive trajectory in mind, I'd love to schedule a meeting to discuss our Q4 strategy \
and how we can best capitalize on this growth. Would you have availability later this week for a \
30-minute session? I'm happy to work around your schedule.

Looking forward to the conversation.

Best regards,
Alex

### Example 2
**Input:**
- Intent: Apologize for a delayed shipment
- Key Facts: Order #4521, delayed by 5 business days, offering 20% discount on next order
- Tone: Empathetic and sincere

**Output:**
<thinking>
The recipient is a frustrated customer. The tone must be empathetic — acknowledge the inconvenience first,
then provide the factual details (order number, delay duration), and close with a goodwill gesture (20% discount).
Avoid corporate jargon. Use warm, human language. Keep it brief — a frustrated customer won't read a wall of text.
Structure: Apologetic subject, empathetic opening, factual middle, resolution + gesture, warm close.
</thinking>

Subject: Our Sincere Apologies for the Delay on Your Order #4521

Dear Jordan,

I want to personally reach out to apologize for the delay with your recent order (#4521). I completely \
understand how frustrating it must be to wait longer than expected, and I'm truly sorry for the inconvenience.

Your shipment has been delayed by approximately 5 business days due to an unexpected logistics issue on \
our end. We are actively tracking it and will send you an updated delivery confirmation as soon as it ships.

To make this right, we'd like to offer you a 20% discount on your next order as a small token of our \
appreciation for your patience. You'll receive the discount code in a separate email shortly.

Thank you for your understanding, and please don't hesitate to reach out if there's anything else I can help with.

Warmly,
Chris
"""

ADVANCED_USER_PROMPT_TEMPLATE = """Please generate a professional email based on the following inputs:

- **Intent**: {intent}
- **Key Facts**:
{key_facts_formatted}
- **Tone**: {tone}

Follow your process: First analyze inside <thinking> tags, then write the final email."""


# --- Strategy B: Basic Prompt (Zero-Shot Direct) ---
BASIC_SYSTEM_PROMPT = """You are a helpful assistant that writes professional emails."""

BASIC_USER_PROMPT_TEMPLATE = """Write a professional email with the following details:

Intent: {intent}
Key Facts:
{key_facts_formatted}
Tone: {tone}

The email should include a Subject line, greeting, body, and sign-off."""


# ============================================================================
# EVALUATION PROMPTS (LLM-as-a-Judge)
# ============================================================================

FACT_RECALL_JUDGE_PROMPT = """You are an expert evaluator. Your task is to determine how many of the \
provided Key Facts are accurately reflected in the Generated Email.

## Input Key Facts:
{key_facts_formatted}

## Generated Email:
{generated_email}

## Instructions:
For each Key Fact, determine if it is semantically present in the email (it does not need to be \
word-for-word, but the core information must be accurately conveyed).

Respond in the following JSON format ONLY (no other text):
{{
  "evaluations": [
    {{"fact": "<fact text>", "present": true/false, "reasoning": "<brief explanation>"}}
  ],
  "total_facts": <number>,
  "facts_recalled": <number>,
  "score": <float between 0.0 and 1.0>
}}"""

TONE_ADHERENCE_JUDGE_PROMPT = """You are an expert evaluator specializing in written communication tone analysis.

## Target Tone: {tone}
## Generated Email:
{generated_email}

## Instructions:
Rate how well the generated email matches the target tone on a scale of 1 to 5:
- 1: Completely mismatched tone (e.g., casual when formal was requested)
- 2: Mostly mismatched with occasional correct elements
- 3: Partially aligned — some sections match, others do not
- 4: Mostly aligned — minor deviations
- 5: Flawless tone alignment throughout

Respond in the following JSON format ONLY (no other text):
{{
  "target_tone": "{tone}",
  "detected_tone_description": "<describe the actual tone of the email>",
  "alignment_reasoning": "<explain why the score was given>",
  "score": <integer between 1 and 5>
}}"""

FORMAT_ADHERENCE_JUDGE_PROMPT = """You are an expert evaluator specializing in professional email formatting.

## Generated Email:
{generated_email}

## Instructions:
Evaluate the structural professionalism and formatting of the email on a scale of 1 to 5:
- Does it have a clear Subject line?
- Does it have a proper greeting/salutation?
- Is the body well-structured with logical paragraph flow?
- Does it have an appropriate sign-off/closing?
- Are there any remaining template placeholders like [Your Name], [Company], [Date], etc.?

Rating scale:
- 1: Missing multiple basic components or contains raw placeholders
- 2: Has some components but structure is disorganized
- 3: Adequate structure with minor issues
- 4: Well-structured with only trivial improvements possible
- 5: Perfectly structured, clean, production-ready email

Respond in the following JSON format ONLY (no other text):
{{
  "has_subject_line": true/false,
  "has_greeting": true/false,
  "has_sign_off": true/false,
  "has_placeholders": true/false,
  "placeholder_examples": ["<list any found>"],
  "structure_reasoning": "<explain the rating>",
  "score": <integer between 1 and 5>
}}"""
