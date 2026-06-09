import json
from pathlib import Path
from typing import Dict, List
import random

BASE_DIR = Path(__file__).resolve().parent.parent
INTENTS_FILE = BASE_DIR / "data" / "intents.json"
GREETINGS_FILE = BASE_DIR / "data" / "greetings.json"

class IntentService:
    def __init__(self):
        self.intents: Dict[str, List[str]] = {}
        self.greetings: Dict[str, List[str]] = {}
        self._load_data()

    def _load_data(self):
        try:
            with open(INTENTS_FILE, "r", encoding="utf-8") as f:
                self.intents = json.load(f)
        except Exception as e:
            self.intents = {}
            
        try:
            with open(GREETINGS_FILE, "r", encoding="utf-8") as f:
                self.greetings = json.load(f)
        except Exception as e:
            self.greetings = {}

    def detect_intent(self, text: str) -> str:
        text_lower = text.lower().strip()
        
        # Remove punctuation for better matching
        import string
        text_clean = text_lower.translate(str.maketrans('', '', string.punctuation))
        words = set(text_clean.split())
        
        # Exact match or strong subset match
        for intent, keywords in self.intents.items():
            for kw in keywords:
                kw_clean = kw.lower().translate(str.maketrans('', '', string.punctuation))
                # Check if keyword is in the text, or if the text is very short and matches
                if kw_clean in text_clean:
                    # To avoid false positives (like 'hi' in 'thigh'), we check word boundaries if it's a short keyword
                    if len(kw_clean) <= 3:
                        if kw_clean in words:
                            return intent
                    else:
                        return intent
                        
        # If no non-symptom intent is found, assume it's symptoms
        return "symptoms"

    def get_greeting_response(self, intent: str) -> str:
        responses = self.greetings.get(intent, ["I am here to help. Please describe your symptoms."])
        return random.choice(responses)

intent_service = IntentService()

def detect_intent(text: str) -> str:
    return intent_service.detect_intent(text)

def get_greeting_response(intent: str) -> str:
    return intent_service.get_greeting_response(intent)
