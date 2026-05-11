from models.inference import predict_similarity
import sys

# We'll suppress some of the verbose loading prints by redirecting stdout temporarily or just let it print.
examples = [
    # --- Exact / Similar Paraphrases ---
    ("The weather is lovely today", "It is a beautiful day outside"),
    ("I am learning how to code", "I am studying programming"),
    ("Can I get a glass of water?", "Could you bring me some water?"),
    
    # --- Very Similar except for a SMALL NEGATIVE part ---
    ("I love going to the beach.", "I don't love going to the beach."),
    ("He is always very helpful and kind.", "He is never very helpful or kind."),
    ("The cat jumped over the tall fence.", "The cat didn't jump over the tall fence."),
    ("The new restaurant is incredibly good.", "The new restaurant is incredibly bad."),
    ("This software works perfectly.", "This software fails perfectly."),
    ("Make sure to always wear a seatbelt.", "Make sure to never wear a seatbelt."),

    # --- Reordered words changing meaning ---
    ("The dog chased the cat.", "The cat chased the dog."),
    ("A man is playing a guitar.", "A guitar is playing a man."),
    
    # --- Subtle numeric or degree differences ---
    ("I have exactly $100.", "I have about $100."),
    ("She passed the exam easily.", "She barely passed the exam.")
]

def main():
    print(f"\n{'-'*110}")
    print(f"{'Sentence 1':<38} | {'Sentence 2':<40} | {'Score':<5} | {'Paraphrase?'}")
    print(f"{'-'*110}")

    for s1, s2 in examples:
        score, is_para = predict_similarity(s1, s2)
        # Format the score to 2 decimal places for easy reading
        print(f"{s1:<38} | {s2:<40} | {score:>5.2f} | {is_para}")
    print(f"{'-'*110}\n")

if __name__ == '__main__':
    main()
