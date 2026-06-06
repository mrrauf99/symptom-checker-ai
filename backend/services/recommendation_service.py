import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "data" / "specialists.json"

with open(FILE_PATH, "r") as file:
    specialists = json.load(file)


def get_specialist(disease: str):

    return specialists.get(
        disease,
        "General Physician"
    )