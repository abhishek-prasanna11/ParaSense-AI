"""
Running thsi testcases before the Build is Approved for deployment
50 diverse examples to stress-test the paraphrase detection backend.
Covers: 
- Simple Paraphrases
- Lexical Overlap (Non-paraphrases)
- Negation traps
- Word-swap (Subject/Object)
- Semantic Near-misses (e.g. arrive vs depart)
- Different levels of formality
"""

import requests
import json

API_URL = "http://localhost:8000/analyze"

EXAMPLES = [
    # --- POSITIVE PARAPHRASES (Expected: True) ---
    {"t1": "The movie was very exciting.", "t2": "It was a really thrilling film.", "exp": True},
    {"t1": "Can you help me with this task?", "t2": "Could you give me a hand with this?", "exp": True},
    {"t1": "The pizza was delicious.", "t2": "The pizza tasted great.", "exp": True},
    {"t1": "I am exhausted.", "t2": "I'm very tired.", "exp": True},
    {"t1": "The store is closed on Sundays.", "t2": "On Sundays, the shop is not open.", "exp": True},
    {"t1": "It's raining cats and dogs.", "t2": "It is pouring outside.", "exp": True},
    {"t1": "She is a talented musician.", "t2": "She has a lot of musical skill.", "exp": True},
    {"t1": "How much does this cost?", "t2": "What is the price of this item?", "exp": True},
    {"t1": "The flight was delayed.", "t2": "The plane is arriving late.", "exp": True},
    {"t1": "He lives in London.", "t2": "London is where he resides.", "exp": True},
    {"t1": "The water is freezing.", "t2": "The water is extremely cold.", "exp": True},
    {"t1": "I forgot my keys.", "t2": "My keys were left behind by mistake.", "exp": True},
    {"t1": "The book is interesting.", "t2": "The novel is quite engaging.", "exp": True},
    {"t1": "They are identical twins.", "t2": "They look exactly the same.", "exp": True},
    {"t1": "The project is finished.", "t2": "The work has been completed.", "exp": True},
    {"t1": "I'll see you later.", "t2": "I'll catch up with you at a later time.", "exp": True},
    {"t1": "The car is expensive.", "t2": "The vehicle costs a lot of money.", "exp": True},
    {"t1": "The sun is shining.", "t2": "It is sunny outside.", "exp": True},
    {"t1": "I need a vacation.", "t2": "I could really use a holiday.", "exp": True},
    {"t1": "The meeting was productive.", "t2": "We got a lot done during the meeting.", "exp": True},
    {"t1": "The soup is hot.", "t2": "The soup has a high temperature.", "exp": True},
    {"t1": "She speaks three languages.", "t2": "She is trilingual.", "exp": True},
    {"t1": "The laptop is broken.", "t2": "The computer isn't working.", "exp": True},
    {"t1": "He is a fast runner.", "t2": "He runs very quickly.", "exp": True},
    {"t1": "The coffee is too sweet.", "t2": "There is too much sugar in the coffee.", "exp": True},

    # --- NEGATIVE (Not Paraphrases) (Expected: False) ---
    {"t1": "The cat is on the mat.", "t2": "The dog is on the mat.", "exp": False},
    {"t1": "I love apples.", "t2": "I hate apples.", "exp": False},
    {"t1": "The sky is blue.", "t2": "The grass is green.", "exp": False},
    {"t1": "He went to the park.", "t2": "He went to the office.", "exp": False},
    {"t1": "The car is red.", "t2": "The car is blue.", "exp": False},
    {"t1": "I am hungry.", "t2": "I am thirsty.", "exp": False},
    {"t1": "She is happy.", "t2": "She is sad.", "exp": False},
    {"t1": "The phone is ringing.", "t2": "The alarm is going off.", "exp": False},
    {"t1": "It is very hot.", "t2": "It is very cold.", "exp": False},
    {"t1": "He is my brother.", "t2": "He is my cousin.", "exp": False},

    # --- ADVERSARIAL TRAPS (Expected: False) ---
    {"t1": "I have been to Paris.", "t2": "I have NOT been to Paris.", "exp": False},
    {"t1": "The experiment was successful.", "t2": "The experiment was a total failure.", "exp": False},
    {"t1": "He is always on time.", "t2": "He is never on time.", "exp": False},
    {"t1": "The dog bit the man.", "t2": "The man bit the dog.", "exp": False},
    {"t1": "John loves Mary.", "t2": "Mary loves John.", "exp": False}, # Semantic flip in some contexts
    {"t1": "The train is arriving.", "t2": "The train is leaving.", "exp": False},
    {"t1": "Switch the lights on.", "t2": "Switch the lights off.", "exp": False},
    {"t1": "The price went up.", "t2": "The price went down.", "exp": False},
    {"t1": "It is safe to enter.", "t2": "It is dangerous to enter.", "exp": False},
    {"t1": "I will definitely come.", "t2": "I might not come.", "exp": False},
    {"t1": "The bottle is full.", "t2": "The bottle is empty.", "exp": False},
    {"t1": "He accepted the offer.", "t2": "He rejected the offer.", "exp": False},
    {"t1": "The door is open.", "t2": "The door is closed.", "exp": False},
    {"t1": "We won the game.", "t2": "We lost the game.", "exp": False},
    {"t1": "The mountain is high.", "t2": "The valley is deep.", "exp": False},
]

# --- ANSI colours ---
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def run_tests():
    print(f"\n{BOLD}Running 50-Example Paraphrase Test Suite...{RESET}\n")
    passed = 0
    
    for i, ex in enumerate(EXAMPLES):
        try:
            resp = requests.post(API_URL, json={"text1": ex["t1"], "text2": ex["t2"]}, timeout=10)
            data = resp.json()
            score = data["similarity"]
            got_para = data["paraphrase"]
            
            is_correct = (got_para == ex["exp"])
            if is_correct:
                passed += 1
                status = f"{GREEN}PASS{RESET}"
            else:
                status = f"{RED}FAIL{RESET}"
            
            print(f"[{i+1:02d}] {status} | Sim: {score:.4f} | Exp: {str(ex['exp']):<5} | Got: {str(got_para):<5}")
            if not is_correct:
                print(f"     T1: {ex['t1']}")
                print(f"     T2: {ex['t2']}")
                
        except Exception as e:
            print(f"[{i+1:02d}] {RED}ERROR{RESET}: {e}")

    print(f"\n{BOLD}{'='*40}{RESET}")
    print(f"{BOLD}Final Result: {passed}/{len(EXAMPLES)} ({(passed/len(EXAMPLES))*100:.1f}%){RESET}")
    print(f"{BOLD}{'='*40}{RESET}\n")

if __name__ == "__main__":
    run_tests()
