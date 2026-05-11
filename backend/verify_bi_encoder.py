import os
from sentence_transformers import SentenceTransformer, util
from models.device import get_device

# Load the newly trained Bi-Encoder
device_str = str(get_device())
model_path = os.path.join(os.path.dirname(__file__), 'models', 'saved_model_mpnet')
model = SentenceTransformer(model_path, device=device_str)

EXAMPLES = [
    {"t1": "The movie was very exciting.", "t2": "It was a really thrilling film.", "exp": True},
    {"t1": "I love going to the beach.", "t2": "I don't love going to the beach.", "exp": False},
    {"t1": "The dog bit the man.", "t2": "The man bit the dog.", "exp": False},
    {"t1": "The medicine is safe for children under twelve.", "t2": "The medicine is NOT safe for children under twelve.", "exp": False},
]

print(f"\n--- Verifying Raw Bi-Encoder Progress ---")
for ex in EXAMPLES:
    emb1 = model.encode(ex["t1"], convert_to_tensor=True)
    emb2 = model.encode(ex["t2"], convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item()
    print(f"T1: {ex['t1']}")
    print(f"T2: {ex['t2']}")
    print(f"Similarity: {score:.4f} | Expected: {ex['exp']}")
    print("-" * 20)
