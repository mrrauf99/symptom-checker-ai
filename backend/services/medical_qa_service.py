import json
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
MEDICAL_QA_FILE = BASE_DIR / "data" / "medical_qa.json"

class MedicalQAService:
    def __init__(self):
        self.qa_data: List[Dict] = []
        self._load_data()

    def _load_data(self):
        try:
            with open(MEDICAL_QA_FILE, "r", encoding="utf-8") as f:
                self.qa_data = json.load(f)
        except Exception:
            self.qa_data = []

    def get_answer(self, text: str) -> Optional[str]:
        text_lower = text.lower().strip()
        
        for qa in self.qa_data:
            for kw in qa.get("keywords", []):
                if kw.lower() in text_lower:
                    return qa.get("answer")
                    
        return "I am a symptom checker AI. I don't have a specific answer for that medical question, but if you describe your symptoms, I can help predict potential conditions."

medical_qa_service = MedicalQAService()

def get_medical_qa_answer(text: str) -> Optional[str]:
    return medical_qa_service.get_answer(text)
