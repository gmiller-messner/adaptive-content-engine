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
            f'  <p class="takeaways-header">Key Takeaways</p>\n'
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


def split_into_parts(content: str) -> list[tuple[str | None, str, str]]:
    """Split processed lesson content into (heading, body, slug) tuples.

    Splits on ## Part headings. First tuple is the intro (heading=None, slug='index').
    Returns: list of (heading_text_or_None, body_content, page_slug)
    """
    pattern = r"^(## Part \d+.*?)$"
    segments = re.split(pattern, content, flags=re.MULTILINE)

    result = []
    intro = segments[0].strip()
    if intro:
        result.append((None, intro, "index"))

    part_num = 1
    i = 1
    while i < len(segments):
        heading = segments[i].strip() if i < len(segments) else ""
        body = segments[i + 1].strip() if i + 1 < len(segments) else ""
        result.append((heading, body, f"part-{part_num}"))
        part_num += 1
        i += 2

    return result


def build_page_nav(parts: list, current_index: int) -> str:
    """Build prev/next navigation HTML for a lesson page."""
    prev_item = parts[current_index - 1] if current_index > 0 else None
    next_item = parts[current_index + 1] if current_index < len(parts) - 1 else None

    prev_slug = prev_item[2] if prev_item else None
    next_slug = next_item[2] if next_item else None

    # Resolve display labels
    prev_label = "Introduction" if prev_slug == "index" else (
        prev_item[0].lstrip("#").strip() if prev_item and prev_item[0] else "Previous"
    )
    next_label = "Introduction" if next_slug == "index" else (
        next_item[0].lstrip("#").strip() if next_item and next_item[0] else "Next"
    )

    # Resolve relative URLs (siblings in same directory; index uses ./)
    prev_url = "./" if prev_slug == "index" else f"../{prev_slug}/" if prev_slug else None
    next_url = "./" if next_slug == "index" else f"../{next_slug}/" if next_slug else None

    if not prev_url and not next_url:
        return ""

    prev_html = (
        f'<a href="{prev_url}" class="lesson-nav-prev">← {prev_label}</a>'
        if prev_url else '<span class="lesson-nav-prev"></span>'
    )
    next_html = (
        f'<a href="{next_url}" class="lesson-nav-next">{next_label} →</a>'
        if next_url else '<span class="lesson-nav-next"></span>'
    )

    return f'\n\n<div class="lesson-nav">{prev_html}{next_html}</div>\n'


def render_lesson(input_path: Path, output_dir: Path, nav_order: int = 1) -> list[Path]:
    content = input_path.read_text(encoding="utf-8")
    title = extract_title(content)
    processed = process_tags(content)
    slug = clean_persona_stem(input_path.stem)
    safe_title = title.replace('"', '\\"')

    parts = split_into_parts(processed)

    # Remove old flat file if it exists from a previous render
    old_flat = output_dir / f"{slug}.md"
    if old_flat.exists():
        old_flat.unlink()

    lesson_dir = output_dir / slug
    lesson_dir.mkdir(parents=True, exist_ok=True)

    output_paths = []

    for i, (heading, body, page_slug) in enumerate(parts):
        is_index = page_slug == "index"

        if is_index:
            front_matter = (
                f"---\n"
                f'title: "{safe_title}"\n'
                f"layout: default\n"
                f"nav_order: {nav_order}\n"
                f"has_children: true\n"
                f"parent: Lessons\n"
                f"---\n\n"
            )
        else:
            part_num = int(page_slug.split("-")[1])
            page_title = heading.lstrip("#").strip() if heading else f"Part {part_num}"
            safe_page_title = page_title.replace('"', '\\"')
            front_matter = (
                f"---\n"
                f'title: "{safe_page_title}"\n'
                f"layout: default\n"
                f"nav_order: {part_num}\n"
                f'parent: "{safe_title}"\n'
                f"grand_parent: Lessons\n"
                f"---\n\n"
            )

        nav_html = build_page_nav(parts, i)
        output = front_matter + body + nav_html

        output_path = lesson_dir / f"{page_slug}.md"
        output_path.write_text(output, encoding="utf-8")
        output_paths.append(output_path)
        print(f"  {input_path.name} → docs/lessons/{slug}/{page_slug}.md")

    return output_paths
