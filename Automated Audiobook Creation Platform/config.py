from pathlib import Path
import os

# Model and API
OPENAI_MODEL = "gpt-4o-mini-tts"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directories
BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "outputs" / "cache"
OUT_DIR = BASE_DIR / "outputs" / "final"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Defaults
CHUNK_MAX_CHARS = 4000
CHUNK_OVERLAP = 200
DEFAULT_VOICE = "alloy"
