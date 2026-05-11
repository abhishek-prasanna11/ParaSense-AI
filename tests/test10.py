"""
10 curated examples to test the paraphrase detection backend.
Covers: true paraphrases, non-paraphrases, negation traps,
        synonymous rewrites, word-order changes, and semantic near-misses.
"""

import requests
import json

API_URL = "http://localhost:8000/analyze"

EXAMPLES = [
    # ── TRUE PARAPHRASES ──────────────────────────────────────────────────────
    {
        "id": 1,
        "label": "True Paraphrase",
        "category": "Synonym rewrite",
        "text1": "The child is playing in the park.",
        "text2": "A kid is having fun at the playground.",
        "expected_paraphrase": True,
    },
    {
        "id": 2,
        "label": "True Paraphrase",
        "category": "Passive ↔ Active voice",
        "text1": "The scientist discovered a new species of bird.",
        "text2": "A new bird species was discovered by the scientist.",
        "expected_paraphrase": True,
    },
    {
        "id": 3,
        "label": "True Paraphrase",
        "category": "Formal ↔ Informal phrasing",
        "text1": "He passed away peacefully last night.",
        "text2": "He died quietly during the night.",
        "expected_paraphrase": True,
    },
    {
        "id": 4,
        "label": "True Paraphrase",
        "category": "Sentence restructuring",
        "text1": "Banks in the city will be closed on Monday due to the public holiday.",
        "text2": "Because of the public holiday, city banks won't open on Monday.",
        "expected_paraphrase": True,
    },
    {
        "id": 5,
        "label": "True Paraphrase",
        "category": "Numerical / unit equivalence",
        "text1": "The temperature dropped to zero degrees Celsius.",
        "text2": "It got as cold as 32 degrees Fahrenheit.",
        "expected_paraphrase": True,
    },
    # ── NON-PARAPHRASES ───────────────────────────────────────────────────────
    {
        "id": 6,
        "label": "Not a Paraphrase",
        "category": "Completely unrelated topics",
        "text1": "She enjoys painting landscapes in her free time.",
        "text2": "The government announced a new tax reform policy.",
        "expected_paraphrase": False,
    },
    {
        "id": 7,
        "label": "Not a Paraphrase",
        "category": "Negation trap",
        "text1": "The medicine is safe for children under twelve.",
        "text2": "The medicine is NOT safe for children under twelve.",
        "expected_paraphrase": False,
    },
    {
        "id": 8,
        "label": "Not a Paraphrase",
        "category": "Similar surface, opposite meaning",
        "text1": "The company reported record profits this quarter.",
        "text2": "The company reported record losses this quarter.",
        "expected_paraphrase": False,
    },
    # ── TRICKY / EDGE CASES ───────────────────────────────────────────────────
    {
        "id": 9,
        "label": "True Paraphrase",
        "category": "Tricky – word-order swap",
        "text1": "John gave Mary a beautiful red rose.",
        "text2": "Mary received a lovely red rose from John.",
        "expected_paraphrase": True,
    },
    {
        "id": 10,
        "label": "Not a Paraphrase",
        "category": "Tricky – same subject, different event",
        "text1": "The train arrived at the station on time.",
        "text2": "The train departed from the station ahead of schedule.",
        "expected_paraphrase": False,
    },
]

# ── ANSI colours ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def run_tests():
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}  Paraphrase Detection — 10-Example Test Suite{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")

    passed = 0
    failed = 0
    results = []

    for ex in EXAMPLES:
        try:
            resp = requests.post(API_URL, json={"text1": ex["text1"], "text2": ex["text2"]}, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            similarity   = data["similarity"]
            is_paraphrase = data["paraphrase"]
            correct = (is_paraphrase == ex["expected_paraphrase"])
        except Exception as e:
            similarity, is_paraphrase, correct = None, None, False
            data = {"error": str(e)}

        status = f"{GREEN}✅ PASS{RESET}" if correct else f"{RED}❌ FAIL{RESET}"
        if correct:
            passed += 1
        else:
            failed += 1

        bar_len = int((similarity or 0) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)

        print(f"{BOLD}[{ex['id']:02d}] {ex['label']}  |  {ex['category']}{RESET}")
        print(f"  Text 1  : {ex['text1']}")
        print(f"  Text 2  : {ex['text2']}")
        print(f"  Expected: {'Paraphrase' if ex['expected_paraphrase'] else 'Not a Paraphrase'}")
        if similarity is not None:
            para_str = f"{YELLOW}Paraphrase{RESET}" if is_paraphrase else "Not a Paraphrase"
            print(f"  Got     : {para_str}  |  Similarity: {similarity:.4f}  [{bar}]")
        else:
            print(f"  Got     : ERROR — {data.get('error')}")
        print(f"  Result  : {status}")
        print()

        results.append({
            "id": ex["id"],
            "category": ex["category"],
            "expected": ex["expected_paraphrase"],
            "got": is_paraphrase,
            "similarity": similarity,
            "correct": correct,
        })

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"{BOLD}{CYAN}{'='*70}{RESET}")
    pct = (passed / len(EXAMPLES)) * 100
    colour = GREEN if pct == 100 else (YELLOW if pct >= 70 else RED)
    print(f"{BOLD}  Final Score: {colour}{passed}/{len(EXAMPLES)} ({pct:.0f}%){RESET}")

    if failed:
        print(f"\n  {RED}Failed cases:{RESET}")
        for r in results:
            if not r["correct"]:
                exp = "Paraphrase" if r["expected"] else "Not Paraphrase"
                got = "Paraphrase" if r["got"] else "Not Paraphrase"
                print(f"    [{r['id']:02d}] {r['category']} — expected {exp}, got {got} (sim={r['similarity']:.4f})")

    print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")

if __name__ == "__main__":
    run_tests()
