import re
from pathlib import Path


def extract_title(content: str) -> str:
    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else "Lesson"


def clean_persona_stem(stem: str) -> str:
    """Convert a timestamped lesson filename stem to a clean URL slug.

    e.g. lesson_alex_chen_software_developer_20260407_085315 -> alex-chen-software-developer
    """
    name = re.sub(r"^lesson_", "", stem)
    name = re.sub(r"_\d{8}_\d{6}$", "", name)
    name = re.sub(r"_\d{8}_recovered$", "", name)
    return name.replace("_", "-")


def format_card_body(body: str) -> str:
    """Add blank lines between field lines so kramdown renders each as its own paragraph."""
    lines = [line.strip() for line in body.strip().split("\n") if line.strip()]
    return "\n\n".join(lines)


def render_attack_cards(content: str) -> str:
    def replace(match):
        name = match.group(1).strip()
        body = format_card_body(match.group(2))
        return (
            f'\n<div class="attack-card" markdown="1">\n'
            f'<div class="attack-card-header">ATTACK MODEL: {name}</div>\n\n'
            f"{body}\n\n"
            f"</div>\n"
        )

    return re.sub(
        r"\[ATTACK MODEL CARD: ([^\]]+)\]\n(.*?)\n\[/ATTACK MODEL CARD\]",
        replace,
        content,
        flags=re.DOTALL,
    )


def render_terms(content: str) -> str:
    def replace(match):
        text = match.group(1).strip()
        if " — " in text:
            term, definition = text.split(" — ", 1)
        elif " - " in text:
            term, definition = text.split(" - ", 1)
        else:
            term, definition = text, ""

        inner = f'<span class="term-badge">TERM</span> <strong>{term.strip()}</strong>'
        if definition:
            inner += f" — {definition.strip()}"

        return f'<span class="term-callout">{inner}</span>'

    return re.sub(r"\[TERM: ([^\]]+)\]", replace, content)


def render_images(content: str) -> str:
    def replace(match):
        description = match.group(1).strip()
        return (
            f'\n<div class="image-placeholder">'
            f'<div class="image-placeholder-label">[ image ]</div>'
            f'<div class="image-placeholder-caption">{description}</div>'
            f"</div>\n"
        )

    return re.sub(r"\[IMAGE: ([^\]]+)\]", replace, content)


def render_takeaways(content: str) -> str:
    def replace(match):
        body = match.group(1).strip()
        return (
            f'\n<div class="takeaways" markdown="1">\n'
            f"**Key Takeaways**\n\n"
            f"{body}\n\n"
            f"</div>\n"
        )

    return re.sub(
        r"\[TAKEAWAYS\]\n(.*?)\n\[/TAKEAWAYS\]",
        replace,
        content,
        flags=re.DOTALL,
    )


def process_tags(content: str) -> str:
    content = render_attack_cards(content)
    content = render_terms(content)
    content = render_images(content)
    content = render_takeaways(content)
    return content


def render_lesson(input_path: Path, output_dir: Path, nav_order: int = 1) -> Path:
    content = input_path.read_text(encoding="utf-8")
    title = extract_title(content)
    processed = process_tags(content)

    front_matter = (
        f"---\n"
        f'title: "{title}"\n'
        f"layout: default\n"
        f"nav_order: {nav_order}\n"
        f"parent: Lessons\n"
        f"---\n\n"
    )

    output = front_matter + processed

    output_dir.mkdir(parents=True, exist_ok=True)
    slug = clean_persona_stem(input_path.stem)
    output_path = output_dir / f"{slug}.md"
    output_path.write_text(output, encoding="utf-8")
    print(f"  {input_path.name} → docs/lessons/{output_path.name}")
    return output_path
