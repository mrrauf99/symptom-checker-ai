import json
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
FAQS_FILE = BASE_DIR / "data" / "faqs.json"

class FAQService:
    def __init__(self):
        self.faqs: List[Dict] = []
        self._load_data()

    def _load_data(self):
        try:
            with open(FAQS_FILE, "r", encoding="utf-8") as f:
                self.faqs = json.load(f)
        except Exception:
            self.faqs = []

    def get_answer(self, text: str) -> Optional[str]:
        text_lower = text.lower().strip()
        
        for faq in self.faqs:
            for kw in faq.get("keywords", []):
                if kw.lower() in text_lower:
                    return faq.get("answer")
                    
        # Fuzzy fallback could be added here
        return None

faq_service = FAQService()

def get_faq_answer(text: str) -> Optional[str]:
    return faq_service.get_answer(text)
