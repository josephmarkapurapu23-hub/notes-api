import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
NOTES_FILE = DATA_DIR / "notes.json"

def ensure_data_file():
    DATA_DIR.mkdir(parents = True, exist_ok = True)
    if not NOTES_FILE.exists():
        NOTES_FILE.write_text("[]", encoding="utf-8")

def load_notes():
    ensure_data_file()
    return json.loads(NOTES_FILE.read_text(encoding = "utf-8"))

def save_notes(notes):
    ensure_data_file()
    NOTES_FILE.write_text(json.dumps(notes, indent = 2), encoding = "utf-8")
    