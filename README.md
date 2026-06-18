# Email Generation Assistant — AI Engineer Assessment

An LLM-powered Email Generation Assistant with advanced prompt engineering, a custom evaluation framework, and a FastAPI backend. Built with the native OpenAI Python SDK and GPT-4o-mini.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Design Decisions & Trade-offs](#design-decisions--trade-offs)
- [Prompt Engineering Strategy](#prompt-engineering-strategy)
- [Custom Evaluation Metrics](#custom-evaluation-metrics)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)

---

## Project Overview

This project generates professional emails from three inputs:
- **Intent**: The core purpose of the email.
- **Key Facts**: Bullet points that must be seamlessly included.
- **Tone**: The desired writing style (formal, casual, urgent, empathetic, etc.).

It includes a full evaluation framework comparing two prompting strategies across 10 test scenarios using 3 custom metrics.

---

## Design Decisions & Trade-offs

| Decision | Rationale |
|---|---|
| **Native OpenAI SDK** (not LangChain) | Single-turn generation doesn't need memory/orchestration. Direct SDK gives full control over prompt formatting — critical for Few-Shot templates and Chain-of-Thought XML tags. |
| **SQLite** (not PostgreSQL/MongoDB) | Zero-configuration database. Runs anywhere without setup. Stored as a local `emails.db` file. Perfect for portable assessments. |
| **File-based evaluation output** (JSON + CSV) | Meets the assessment requirement for structured output files. Easy to version-control and review. |
| **LLM-as-a-Judge** (not BLEU/ROUGE) | Traditional NLP metrics poorly evaluate creative text generation. LLM judges can assess semantic fact inclusion, tone alignment, and structural quality far more accurately. |

---

## Prompt Engineering Strategy

### Strategy A: Advanced (Role-Playing + Few-Shot + Chain-of-Thought)
The advanced prompt template uses three layered techniques:
1. **Persona Role-Playing**: Assigns the LLM the role of an "Expert Executive Communications Director with 20 years of experience."
2. **Few-Shot Examples**: Includes 2 complete input → thought → email examples demonstrating the expected format and quality.
3. **Chain-of-Thought (CoT)**: Requires the model to first analyze the inputs inside `<thinking>` tags before generating the email.

### Strategy B: Basic (Zero-Shot Direct)
A simple, direct instruction: "Write a professional email with this intent, facts, and tone." Used as a baseline for comparison.

---

## Custom Evaluation Metrics

### 1. Fact Recall & Integration Accuracy (Score: 0.0 – 1.0)
- **Definition**: Measures the percentage of input Key Facts semantically present in the generated email.
- **Methodology**: LLM-as-a-Judge evaluates each fact for semantic presence (not just keyword matching).
- **Formula**: `Score = Facts Recalled / Total Facts`

### 2. Tone Adherence Score (Score: 1 – 5)
- **Definition**: Evaluates whether vocabulary, sentence pacing, and emotional markers match the target tone.
- **Methodology**: LLM-as-a-Judge rates alignment with detailed reasoning.

### 3. Structural Professionalism & Formatting (Score: 1 – 5)
- **Definition**: Checks for proper email structure (Subject, Greeting, Sign-off) and absence of template placeholders.
- **Methodology**: Hybrid — 50% programmatic regex checks + 50% LLM-as-a-Judge assessment.

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- An OpenAI API key

### Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd New_project

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file in the project root:
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

---

## Running the Project

### Option 1: Run the CLI Evaluation
```bash
python run_evaluation.py
```
This will:
- Generate emails for all 10 scenarios using both strategies
- Evaluate each with 3 custom metrics
- Output `evaluation_results.json` and `evaluation_results.csv`
- Print a summary table to the console

### Option 2: Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```
Then visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

### API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/email/generate` | Generate a professional email |
| `POST` | `/api/v1/evaluation/run` | Run the full 10-scenario benchmark |
| `GET` | `/health` | Health check |

---

## Project Structure

```
New_project/
├── .env                          # API credentials (not committed)
├── .gitignore                    # Git ignore rules
├── .github/workflows/ci.yml     # GitHub Actions CI pipeline
├── requirements.txt              # Python dependencies
├── config.py                     # API setup & prompt templates
├── email_generator.py            # Core email generation engine
├── evaluation_scenarios.py       # 10 test scenarios + human references
├── evaluation_metrics.py         # 3 custom evaluation metrics
├── run_evaluation.py             # CLI evaluation runner
├── app/                          # FastAPI application
│   ├── main.py                   # App initialization
│   ├── database.py               # SQLite + SQLAlchemy config
│   ├── models/
│   │   └── email_log.py          # ORM model for email logs
│   ├── schemas/
│   │   ├── email.py              # Request/Response schemas
│   │   └── evaluation.py         # Evaluation result schemas
│   └── api/routes/
│       ├── email.py              # POST /api/v1/email/generate
│       └── evaluation.py         # POST /api/v1/evaluation/run
├── tests/                        # Unit tests
├── evaluation_results.json       # Generated: Full evaluation report
├── evaluation_results.csv        # Generated: Summary scores table
└── comparative_analysis.md       # Model comparison analysis
```
