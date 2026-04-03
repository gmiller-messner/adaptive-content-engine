from dotenv import load_dotenv
from pathlib import Path
from generator import generate_lesson

load_dotenv()

# --- Hardcoded inputs (Stage 3 scaffold) ---
BASE_DIR = Path(__file__).parent
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR.parent / "outputs"

SOURCE_DOCUMENT = INPUTS_DIR / "source_document.md"
PERSONA = INPUTS_DIR / "persona_alex_chen_software_developer.md"
# -------------------------------------------

if __name__ == "__main__":
    generate_lesson(
        source_path=SOURCE_DOCUMENT,
        persona_path=PERSONA,
        output_dir=OUTPUT_DIR,
    )
