import argparse
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
SHARED_DIR = CONTENT_DIR / "_shared"
OUTPUTS_DIR = BASE_DIR / "outputs"
DOCS_LESSONS_DIR = BASE_DIR / "docs" / "lessons"

SHARED_STYLE_STANDARDS = SHARED_DIR / "style_standards.md"


def discover_sets() -> list[str]:
    """Return the names of available content sets (subdirs of content/, excluding _shared)."""
    if not CONTENT_DIR.exists():
        return []
    return sorted(
        d.name
        for d in CONTENT_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    )


def resolve_sets(args) -> list[str] | None:
    """Resolve the --set / --all-sets selection into a list of set names.

    Returns None (and prints guidance) when the selection is invalid or empty.
    """
    available = discover_sets()
    if not available:
        print(f"No content sets found in {CONTENT_DIR}/")
        return None

    if getattr(args, "all_sets", False):
        return available

    if getattr(args, "set", None):
        if args.set not in available:
            print(f"Unknown set: {args.set!r}")
            print("Available sets: " + ", ".join(available))
            return None
        return [args.set]

    print("Specify a content set with --set <name>, or --all-sets for every set.")
    print("Available sets: " + ", ".join(available))
    return None


def cmd_generate(args):
    from stage3_lesson_generation.generator import generate_lesson

    sets = resolve_sets(args)
    if sets is None:
        return

    for set_name in sets:
        set_dir = CONTENT_DIR / set_name
        source = set_dir / "source_document.md"
        if not source.exists():
            print(f"[{set_name}] skipped — no source_document.md")
            continue

        objectives = set_dir / "learning_objectives.md"
        examples = set_dir / "examples_bank.md"
        personas = sorted((set_dir / "personas").glob("*.md"))
        if not personas:
            print(f"[{set_name}] skipped — no personas in personas/")
            continue

        set_output_dir = OUTPUTS_DIR / set_name
        print(f"\n=== Set: {set_name} — {len(personas)} persona(s) ===")
        for persona in personas:
            generate_lesson(
                source_path=source,
                persona_path=persona,
                output_dir=set_output_dir,
                examples_path=examples if examples.exists() else None,
                learning_objectives_path=objectives if objectives.exists() else None,
                style_standards_path=(
                    SHARED_STYLE_STANDARDS if SHARED_STYLE_STANDARDS.exists() else None
                ),
            )


def cmd_render(args):
    from stage4_rendering.renderer import render_lesson

    sets = resolve_sets(args)
    if sets is None:
        return

    # Offset each set's nav_order by its rank among all sets, so lessons group by
    # topic in the site nav and never collide across sets (llm-security -> 1,2,3;
    # next set -> 101,102; ...). Rank comes from the full set list, so ordering is
    # stable even when rendering a single set.
    all_sets = discover_sets()
    NAV_ORDER_PER_SET = 100

    for set_name in sets:
        set_rank = all_sets.index(set_name)
        set_output_dir = OUTPUTS_DIR / set_name
        all_lessons = list(set_output_dir.glob("lesson_*.md"))
        if not all_lessons:
            print(f"[{set_name}] no lesson files in {set_output_dir}/")
            continue

        persona_files: dict[str, list[Path]] = {}
        for f in all_lessons:
            persona = re.sub(r"^lesson_", "", f.stem)
            persona = re.sub(r"_\d{8}_\d{6}$", "", persona)
            persona = re.sub(r"_\d{8}_recovered$", "", persona)
            persona_files.setdefault(persona, []).append(f)

        latest = sorted(
            [max(files, key=lambda f: f.stat().st_mtime) for files in persona_files.values()],
            key=lambda f: f.stem,
        )

        print(f"\n=== Set: {set_name} — rendering {len(latest)} lesson(s) ===")
        for i, lesson_path in enumerate(latest, start=1):
            nav_order = set_rank * NAV_ORDER_PER_SET + i
            render_lesson(lesson_path, DOCS_LESSONS_DIR, nav_order=nav_order, set_name=set_name)


def cmd_all(args):
    cmd_generate(args)
    print()
    cmd_render(args)


def add_set_args(subparser):
    group = subparser.add_mutually_exclusive_group()
    group.add_argument("--set", help="Content set to run (see content/)")
    group.add_argument(
        "--all-sets", action="store_true", help="Run every content set"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Adaptive Content Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "commands:\n"
            "  generate   Generate lessons for a content set\n"
            "  render     Render lessons to GitHub Pages markdown\n"
            "  all        Generate then render\n"
            "  sets       List available content sets\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_set_args(subparsers.add_parser("generate", help="Generate lessons for a content set"))
    add_set_args(subparsers.add_parser("render", help="Render lessons to GitHub Pages markdown"))
    add_set_args(subparsers.add_parser("all", help="Generate then render"))
    subparsers.add_parser("sets", help="List available content sets")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "render":
        cmd_render(args)
    elif args.command == "all":
        cmd_all(args)
    elif args.command == "sets":
        available = discover_sets()
        if available:
            print("Available content sets:")
            for name in available:
                print(f"  {name}")
        else:
            print(f"No content sets found in {CONTENT_DIR}/")
            sys.exit(1)


if __name__ == "__main__":
    main()
