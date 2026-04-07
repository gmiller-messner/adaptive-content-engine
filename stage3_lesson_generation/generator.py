import anthropic
from pathlib import Path
from datetime import datetime

SYSTEM_PROMPT = """You are an expert instructional designer who creates tailored learning content.

Given a source document and a learner persona, generate a focused, engaging lesson that meets the learner where they are — using appropriate language, relevant examples, and the right level of technical depth for their background and role.

Structure the lesson with:
- A brief introduction that connects the topic to the learner's specific context
- Core concepts explained at the right technical level for this persona
- Concrete examples drawn from the learner's actual work environment and tools
- Practical, actionable takeaways they can apply immediately
- A brief summary

Do not include preamble or meta-commentary about the lesson. Begin the lesson directly."""


def generate_lesson(
    source_path: Path,
    persona_path: Path,
    output_dir: Path,
    examples_path: Path | None = None,
    learning_objectives_path: Path | None = None,
    style_standards_path: Path | None = None,
) -> Path:
    client = anthropic.Anthropic()

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
        learning_objectives = learning_objectives_path.read_text(encoding="utf-8")
        objectives_block = f"""
Here are the learning objectives this lesson should meet:

<learning_objectives>
{learning_objectives}
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
        model="claude-opus-4-6",
        max_tokens=4096,
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

    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"lesson_{persona_path.stem.replace('persona_', '')}_{timestamp}.md"
    output_path = output_dir / output_filename
    output_path.write_text(lesson_text, encoding="utf-8")

    print(f"Saved to: {output_path}")
    return output_path
