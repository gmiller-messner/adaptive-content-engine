# Adaptive Content Engine

A staged agentic pipeline that generates tailored learning content from source documents and learner personas using the Anthropic API.

## What It Does

Given a source document and a learner persona, the engine generates a lesson customized to that learner's role, technical level, existing knowledge, and specific risk exposure. The same source material produces meaningfully different lessons for a software developer, an engineering manager, or a product manager — because the right lesson for each person is not the same lesson.

The engine is topic-agnostic. Each subject lives in its own **content set** under `content/`, so you can generate lessons for any number of source documents without touching code.

## Pipeline Architecture

This project is structured as a staged pipeline. Each stage is designed to be developed and demonstrated independently.

| Stage | Description | Status |
|---|---|---|
| Stage 1 | Document ingestion and preprocessing | Planned |
| Stage 2 | Persona parsing and enrichment | Planned |
| **Stage 3** | **Lesson generation** | **Built** |
| **Stage 4** | **Rendering to GitHub Pages** | **Built** |

Stage 3 takes a source document and a persona profile, calls the Anthropic API (Claude Opus 4.8 with adaptive thinking), and streams a tailored lesson to the console and an output file. Stage 4 renders the tagged lesson markdown into GitHub Pages-compatible pages.

## Project Structure

```
adaptive-content-engine/
├── README.md
├── requirements.txt
├── .env.example
├── run.py                            # Entry point (generate / render / all / sets)
├── content/                          # One folder per topic ("content set")
│   ├── _shared/
│   │   └── style_standards.md        # Topic-agnostic, applied to every set
│   └── llm-security/
│       ├── source_document.md        # Required
│       ├── learning_objectives.md    # Optional
│       ├── examples_bank.md          # Optional
│       └── personas/
│           ├── alex_chen_software_developer.md
│           ├── jordan_williams_engineering_manager.md
│           └── morgan_lee_vibe_coder.md
├── outputs/                          # Generated lessons, namespaced by set
│   └── llm-security/
├── stage3_lesson_generation/
│   └── generator.py                  # API call and lesson generation
└── stage4_rendering/
    └── renderer.py                   # Tag processing + GitHub Pages markdown
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

### Running the Engine

All commands run from the project root via `run.py`:

```bash
python run.py sets                        # list available content sets
python run.py generate --set llm-security # generate lessons for one set
python run.py generate --all-sets         # generate for every set
python run.py render --set llm-security    # render a set to GitHub Pages markdown
python run.py all --set llm-security       # generate then render
```

`generate` produces one lesson per persona in the set. Each lesson streams to your terminal as it generates, then saves to `outputs/<set>/`. Running `generate` with no `--set`/`--all-sets` prints the available sets rather than generating everything.

### Adaptive Learning Objectives

A set's `learning_objectives.md` holds generic, topic-level objectives. Before writing each lesson, the engine runs a lightweight adaptation call (Claude Sonnet 4.6) that rewrites those generic objectives for the specific persona — their role, tools, and risk exposure. The adapted objectives are saved as `outputs/<set>/objectives_<persona>_<timestamp>.md` (alongside the lesson they drove) and fed into the lesson-generation call. If a set has no `learning_objectives.md`, this step is skipped.

### Adding a New Topic

Create a new content set — no code changes required:

```
content/<your-topic>/
├── source_document.md        # required
├── learning_objectives.md    # optional
├── examples_bank.md          # optional
└── personas/
    ├── persona_one.md
    └── persona_two.md
```

Then run `python run.py generate --set <your-topic>`. Style standards in `content/_shared/style_standards.md` are applied to every set automatically.

### Example Output

Running Stage 3 with the included source document (LLM Security Threats) and the Alex Chen persona produces a technically detailed lesson covering prompt injection and supply chain vulnerabilities, with examples drawn from Alex's actual stack — LangChain, LiteLLM, pip, and CI/CD pipelines.

The same source document run against the Jordan Williams persona produces a lesson focused on data stewardship, shadow AI risk, and the exposure created by feeding sensitive personnel data into unvetted tools — no code, no package managers.

## Requirements

- Python 3.9+
- Anthropic API key ([get one here](https://console.anthropic.com))
