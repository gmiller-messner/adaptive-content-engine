import anthropic
from pathlib import Path
from datetime import datetime

# Model used for the lightweight objectives-adaptation pre-step. Kept separate
# from the lesson model so it can be tuned independently (e.g. Haiku for cost).
ADAPT_MODEL = "claude-sonnet-4-6"

ADAPT_SYSTEM_PROMPT = """You are an expert instructional designer.

You are given a set of generic, topic-level learning objectives and a learner persona. Rewrite the generic objectives into a set of objectives tailored to this specific learner — reframing each in terms of their role, their existing knowledge, the tools they actually use, and their specific risk exposure.

Guidelines:
- Preserve the underlying concepts; adapt the framing, depth, and examples to the learner.
- Make each objective concrete and measurable for this persona (name real tools and situations from their world where relevant).
- Add, merge, or split objectives where the persona's context warrants it — do not pad to match the original count.
- Output only the adapted objectives as a markdown list under a short heading. No preamble, no commentary."""

SYSTEM_PROMPT = """You are an expert instructional designer who creates tailored learning content.

Given a source document and a learner persona, generate a focused, engaging lesson that meets the learner where they are — using appropriate language, relevant examples, and the right level of technical depth for their background and role.

Structure the lesson with:
- A brief introduction that connects the topic to the learner's specific context
- Core concepts explained at the right technical level for this persona
- Concrete examples drawn from the learner's actual work environment and tools
- Practical, actionable takeaways they can apply immediately
- A brief summary

Do not include preamble or meta-commentary about the lesson. Begin the lesson directly."""


def adapt_objectives(
    client: anthropic.Anthropic, generic_objectives: str, persona_profile: str
) -> str:
    """Adapt generic, topic-level objectives to a specific persona (cheap pre-step)."""
    user_message = f"""Here are the generic, topic-level learning objectives:

<generic_objectives>
{generic_objectives}
</generic_objectives>

Here is the learner persona to adapt them for:

<persona_profile>
{persona_profile}
</persona_profile>

Adapt these objectives to this specific learner."""

    response = client.messages.create(
        model=ADAPT_MODEL,
        max_tokens=2000,
        system=ADAPT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return next(
        (block.text for block in response.content if block.type == "text"), ""
    ).strip()


def generate_lesson(
    source_path: Path,
    persona_path: Path,
    output_dir: Path,
    examples_path: Path | None = None,
    learning_objectives_path: Path | None = None,
    style_standards_path: Path | None = None,
) -> Path:
    client = anthropic.Anthropic()

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    persona_slug = persona_path.stem.replace("persona_", "")

    source_document = source_path.read_text(encoding="utf-8")
    persona_profile = persona_path.read_text(encoding="utf-8")

    examples_block = ""
    if examples_path and examples_path.exists():
        examples_bank = examples_path.read_text(encoding="utf-8")
        examples_block = f"""
Here is a bank of real-world examples you may draw from when illustrating concepts:

<examples_bank>
{examples_bank}
</examples_bank>
"""

    objectives_block = ""
    if learning_objectives_path and learning_objectives_path.exists():
        generic_objectives = learning_objectives_path.read_text(encoding="utf-8")

        print(f"Adapting objectives for: {persona_path.stem}")
        adapted_objectives = adapt_objectives(client, generic_objectives, persona_profile)
        objectives_out = output_dir / f"objectives_{persona_slug}_{timestamp}.md"
        objectives_out.write_text(adapted_objectives, encoding="utf-8")
        print(f"Saved adapted objectives to: {objectives_out}")

        objectives_block = f"""
Here are the learning objectives for this specific learner:

<learning_objectives>
{adapted_objectives}
</learning_objectives>
"""

    style_block = ""
    if style_standards_path and style_standards_path.exists():
        style_standards = style_standards_path.read_text(encoding="utf-8")
        style_block = f"""
Here are the style standards to follow when writing the lesson:

<style_standards>
{style_standards}
</style_standards>
"""

    user_message = f"""Here is the source document to teach from:

<source_document>
{source_document}
</source_document>

Here is the learner persona:

<persona_profile>
{persona_profile}
</persona_profile>
{examples_block}{objectives_block}
Generate a tailored lesson for this learner based on the source document.{style_block}"""

    print(f"\nGenerating lesson for: {persona_path.stem}")
    print("-" * 60)

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        response = stream.get_final_message()

    print("\n" + "-" * 60)

    lesson_text = next(
        (block.text for block in response.content if block.type == "text"), ""
    )

    output_filename = f"lesson_{persona_slug}_{timestamp}.md"
    output_path = output_dir / output_filename
    output_path.write_text(lesson_text, encoding="utf-8")

    print(f"Saved to: {output_path}")
    return output_path
