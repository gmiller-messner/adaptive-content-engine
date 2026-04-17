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


def attr(value: str) -> str:
    """Escape a string for safe use inside an HTML attribute value."""
    return value.replace("&", "&amp;").replace('"', "&quot;")


def md_to_html_inline(text: str) -> str:
    """Convert inline markdown (bold, italic, code) to HTML."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def format_card_body(body: str) -> str:
    """Convert card body plain-text field lines to HTML paragraphs.

    Expects lines in the format 'Field name: value'.
    The field label is wrapped in <strong>; the value is plain text.
    """
    lines = [line.strip() for line in body.strip().split("\n") if line.strip()]
    html_lines = []
    for line in lines:
        match = re.match(r"^([^:]+):\s*(.*)$", line)
        if match:
            label, value = match.group(1).strip(), match.group(2).strip()
            html_lines.append(f"<p><strong>{label}:</strong> {value}</p>")
        else:
            html_lines.append(f"<p>{line}</p>")
    return "\n".join(html_lines)


def render_attack_cards(content: str) -> str:
    def replace(match):
        name = match.group(1).strip()
        body = format_card_body(match.group(2))
        return (
            f'\n<div class="attack-card" data-name="{attr(name)}">\n'
            f"{body}\n"
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
        description = attr(match.group(1).strip())
        return (
            f'\n\n<div class="image-placeholder" data-caption="{description}"></div>\n\n'
        )

    return re.sub(r"\[IMAGE: ([^\]]+)\]", replace, content)


def render_takeaways(content: str) -> str:
    def replace(match):
        body = match.group(1).strip()
        lines = [line.strip() for line in body.split("\n") if line.strip()]
        items = []
        for line in lines:
            text = re.sub(r"^[-*]\s*", "", line)
            items.append(f"  <li>{md_to_html_inline(text)}</li>")
        list_html = "\n".join(items)
        return (
            f'\n<div class="takeaways">\n'
            f"  <p class=\"takeaways-header\">Key Takeaways</p>\n"
            f"  <ul>\n{list_html}\n  </ul>\n"
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

    safe_title = title.replace('"', '\\"')
    front_matter = (
        f"---\n"
        f'title: "{safe_title}"\n'
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
