import os
import random
from datasets import load_dataset
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from models.device import get_device

def generate_synthetic_negatives(texts, count=1000):
    """
    Generates diverse negation and swap patterns from existing texts.
    """
    negations = ["not ", "never ", "fails to ", "does not ", "didn't ", "hardly "]
    synthetic = []
    
    for _ in range(count):
        text = random.choice(texts)
        words = text.split()
        if len(words) < 4: continue
        
        # 1. Simple negation insertion
        idx = random.randint(0, len(words)-1)
        neg_text = words[:idx] + [random.choice(negations)] + words[idx:]
        synthetic.append(InputExample(texts=[text, " ".join(neg_text)], label=0.0))
        
        # 2. Word swap (subject/object style)
        if len(words) > 5:
            w1, w2 = random.sample(range(len(words)), 2)
            swapped = words[:]
            swapped[w1], swapped[w2] = swapped[w2], swapped[w1]
            synthetic.append(InputExample(texts=[text, " ".join(swapped)], label=0.0))
            
    return synthetic

def train_transformer_model():
    device_str = str(get_device())
    print(f"Using device: {device_str}")
    
    # Load Sentence-BERT
    model = SentenceTransformer('all-mpnet-base-v2', device=device_str)

    train_examples = []

    # 1. Load QQP (General Paraphrase)
    print("Loading QQP dataset...")
    qqp = load_dataset("glue", "qqp", split="train[:30000]")
    for row in qqp:
        train_examples.append(InputExample(texts=[row['question1'], row['question2']], label=float(row['label'])))

    # 2. Load PAWS (Word-swap adversaries)
    print("Loading PAWS dataset...")
    try:
        paws = load_dataset("paws", "labeled_final", split="train[:10000]")
        for row in paws:
            train_examples.append(InputExample(texts=[row['sentence1'], row['sentence2']], label=float(row['label'])))
    except Exception as e:
        print(f"Skipping PAWS: {e}")

    # 3. Load MNLI (Negation/Contradiction logic)
    print("Loading MNLI dataset...")
    try:
        mnli = load_dataset("multi_nli", split="train[:10000]")
        for row in mnli:
            # 0: entailment (pos), 2: contradiction (neg)
            if row['label'] == 0:
                train_examples.append(InputExample(texts=[row['premise'], row['hypothesis']], label=1.0))
            elif row['label'] == 2:
                train_examples.append(InputExample(texts=[row['premise'], row['hypothesis']], label=0.0))
    except Exception as e:
        print(f"Skipping MNLI: {e}")

    # 4. Add Synthetic Negatives
    print("Generating diverse synthetic negatives...")
    all_texts = [row['question1'] for row in qqp] + [row['question2'] for row in qqp]
    train_examples.extend(generate_synthetic_negatives(all_texts, count=2000))

    # Define DataLoader
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

    # Use ContrastiveLoss
    train_loss = losses.ContrastiveLoss(model=model)

    print(f"Starting training on {len(train_examples)} examples...")
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        warmup_steps=500,
        weight_decay=0.01,
        show_progress_bar=True
    )
    
    # Save the model
    output_path = os.path.join(os.path.dirname(__file__), 'saved_model_mpnet')
    print(f"Saving improved model to {output_path}...")
    model.save(output_path)
    print("Training completed.")

if __name__ == "__main__":
    train_transformer_model()
