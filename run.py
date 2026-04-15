import argparse
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
INPUTS_DIR = BASE_DIR / "stage3_lesson_generation" / "inputs"
OUTPUTS_DIR = BASE_DIR / "outputs"
DOCS_LESSONS_DIR = BASE_DIR / "docs" / "lessons"

SOURCE_DOCUMENT = INPUTS_DIR / "source_document.md"
EXAMPLES_BANK = INPUTS_DIR / "examples_bank.md"
LEARNING_OBJECTIVES = INPUTS_DIR / "learning_objectives.md"
STYLE_STANDARDS = INPUTS_DIR / "style_standards.md"


def cmd_generate():
    from stage3_lesson_generation.generator import generate_lesson

    personas = sorted(INPUTS_DIR.glob("persona_*.md"))
    if not personas:
        print("No persona files found in inputs/")
        return

    print(f"Generating lessons for {len(personas)} persona(s)...\n")
    for persona in personas:
        generate_lesson(
            source_path=SOURCE_DOCUMENT,
            persona_path=persona,
            output_dir=OUTPUTS_DIR,
            examples_path=EXAMPLES_BANK,
            learning_objectives_path=LEARNING_OBJECTIVES,
            style_standards_path=STYLE_STANDARDS,
        )


def cmd_render():
    from stage4_rendering.renderer import render_lesson

    all_lessons = list(OUTPUTS_DIR.glob("lesson_*.md"))

    persona_files: dict[str, list[Path]] = {}
    for f in all_lessons:
        stem = f.stem
        persona = re.sub(r"^lesson_", "", stem)
        persona = re.sub(r"_\d{8}_\d{6}$", "", persona)
        persona = re.sub(r"_\d{8}_recovered$", "", persona)
        persona_files.setdefault(persona, []).append(f)

    latest = sorted(
        [max(files, key=lambda f: f.stat().st_mtime) for files in persona_files.values()],
        key=lambda f: f.stem,
    )

    if not latest:
        print("No lesson files found in outputs/")
        return

    print(f"Rendering {len(latest)} lesson(s) to docs/lessons/\n")
    for i, lesson_path in enumerate(latest, start=1):
        render_lesson(lesson_path, DOCS_LESSONS_DIR, nav_order=i)


def cmd_all():
    cmd_generate()
    print()
    cmd_render()


def main():
    parser = argparse.ArgumentParser(
        description="Adaptive Content Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "commands:\n"
            "  generate   Generate lessons for all personas\n"
            "  render     Render lessons to GitHub Pages markdown\n"
            "  all        Generate then render\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("generate", help="Generate lessons for all personas")
    subparsers.add_parser("render", help="Render lessons to GitHub Pages markdown")
    subparsers.add_parser("all", help="Generate then render")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate()
    elif args.command == "render":
        cmd_render()
    elif args.command == "all":
        cmd_all()


if __name__ == "__main__":
    main()
