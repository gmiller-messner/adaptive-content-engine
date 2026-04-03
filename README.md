# Adaptive Content Engine

A staged agentic pipeline that generates tailored learning content from source documents and learner personas using the Anthropic API.

## What It Does

Given a source document and a learner persona, the engine generates a lesson customized to that learner's role, technical level, existing knowledge, and specific risk exposure. The same source material produces meaningfully different lessons for a software developer, an engineering manager, or a product manager — because the right lesson for each person is not the same lesson.

## Pipeline Architecture

This project is structured as a staged pipeline. Each stage is designed to be developed and demonstrated independently.

| Stage | Description | Status |
|---|---|---|
| Stage 1 | Document ingestion and preprocessing | Planned |
| Stage 2 | Persona parsing and enrichment | Planned |
| **Stage 3** | **Lesson generation** | **Built** |
| Stage 4 | Output formatting and delivery | Planned |

## Stage 3: Lesson Generation

Stage 3 takes a source document and a persona profile as inputs, calls the Anthropic API (Claude Opus 4.6 with adaptive thinking), and streams a tailored lesson to the console and an output file.

### Project Structure

```
adaptive-content-engine/
├── README.md
├── requirements.txt
├── .env.example
├── outputs/                          # Generated lessons land here
└── stage3_lesson_generation/
    ├── run.py                        # Entry point
    ├── generator.py                  # API call and lesson generation
    └── inputs/
        ├── source_document.md
        ├── persona_alex_chen_software_developer.md
        ├── persona_jordan_williams_engineering_manager.md
        └── persona_morgan_lee_vibe_coder.md
```

### Setup

**1. Clone the repository and navigate to the project root.**

**2. Create a `.env` file from the example:**
```bash
cp .env.example .env
```
Then open `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your-api-key-here
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Lesson Generator

Navigate to the `stage3_lesson_generation` directory and run:
```bash
cd stage3_lesson_generation
python run.py
```

The lesson will stream to your terminal as it generates, then save as a Markdown file in the `outputs/` directory.

### Switching Personas

To generate a lesson for a different persona, open `run.py` and update the `PERSONA` variable:

```python
# Alex Chen — Software Developer
PERSONA = INPUTS_DIR / "persona_alex_chen_software_developer.md"

# Jordan Williams — Engineering Manager
# PERSONA = INPUTS_DIR / "persona_jordan_williams_engineering_manager.md"

# Morgan Lee — Vibe-Coder / Product Manager
# PERSONA = INPUTS_DIR / "persona_morgan_lee_vibe_coder.md"
```

### Example Output

Running Stage 3 with the included source document (LLM Security Threats) and the Alex Chen persona produces a technically detailed lesson covering prompt injection and supply chain vulnerabilities, with examples drawn from Alex's actual stack — LangChain, LiteLLM, pip, and CI/CD pipelines.

The same source document run against the Jordan Williams persona produces a lesson focused on data stewardship, shadow AI risk, and the exposure created by feeding sensitive personnel data into unvetted tools — no code, no package managers.

## Requirements

- Python 3.9+
- Anthropic API key ([get one here](https://console.anthropic.com))
