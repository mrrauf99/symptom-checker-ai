import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.chat_service import process_chat_message

def run_tests():
    test_cases = [
        "Hi what's up?",
        "who are you",
        "what is a fever",
        "i don't feel good",
        "i have a severe headache and a high fever",
        "I have some mild chest pain"
    ]
    
    for tc in test_cases:
        print(f"\n--- Testing: '{tc}' ---")
        try:
            res = process_chat_message(session_id="test_sess", content=tc)
            msg = res.get("message")
            res_type = res.get("type")
            
            print(f"Response type: {res_type}")
            print(f"Response message: {msg[:100]}..." if msg and len(msg) > 100 else f"Response message: {msg}")
            print("Has prediction data:", "prediction" in res)
            if "prediction" in res:
                print(f"Prediction: {res['prediction']} ({res['confidence']}%)")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # We need to bypass DB calls if DB is not setup in test, but chat_service uses create_message
    # Let's mock create_message and save_prediction to just print
    import backend.services.chat_service
    backend.services.chat_service.create_message = lambda *args, **kwargs: print(f"[DB MOCK] Saved message role={kwargs.get('role')}")
    backend.services.chat_service.save_prediction = lambda *args, **kwargs: print("[DB MOCK] Saved prediction")
    
    run_tests()
