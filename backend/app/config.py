import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for env_file in (PROJECT_ROOT / ".env", PROJECT_ROOT / ".env.example"):
    if env_file.exists():
        load_dotenv(env_file)

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
