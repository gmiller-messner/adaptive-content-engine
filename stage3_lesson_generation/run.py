from dotenv import load_dotenv
from pathlib import Path
from generator import generate_lesson

load_dotenv()

# --- Hardcoded inputs (Stage 3 scaffold) ---
BASE_DIR = Path(__file__).parent
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR.parent / "outputs"

SOURCE_DOCUMENT = INPUTS_DIR / "source_document.md"
EXAMPLES_BANK = INPUTS_DIR / "examples_bank.md"
LEARNING_OBJECTIVES = INPUTS_DIR / "learning_objectives.md"
STYLE_STANDARDS = INPUTS_DIR / "style_standards.md"
# -------------------------------------------

if __name__ == "__main__":
    personas = sorted(INPUTS_DIR.glob("persona_*.md"))
    for persona in personas:
        generate_lesson(
            source_path=SOURCE_DOCUMENT,
            persona_path=persona,
            output_dir=OUTPUT_DIR,
            examples_path=EXAMPLES_BANK,
            learning_objectives_path=LEARNING_OBJECTIVES,
            style_standards_path=STYLE_STANDARDS,
        )
