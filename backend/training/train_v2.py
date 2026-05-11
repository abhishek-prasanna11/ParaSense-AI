import os
import random
import torch
from datasets import load_dataset
from sentence_transformers import SentenceTransformer, InputExample, losses, models, util
from torch.utils.data import DataLoader
from models.device import get_device
from tqdm import tqdm

def train_multi_task_model():
    device_str = str(get_device())
    print(f"Using device: {device_str}")
    
    # 1. Initialize Student Model (MPNet)
    # We start from the base model to avoid any previous overfitting bias
    model = SentenceTransformer('all-mpnet-base-v2', device=device_str)

    train_examples = []

    # --- 2. Dataset Mega-Mix ---

    # A. QQP (Conversational questions)
    print("Loading QQP...")
    qqp = load_dataset("glue", "qqp", split="train[:30000]")
    for row in qqp:
        train_examples.append(InputExample(texts=[row['question1'], row['question2']], label=float(row['label'])))

    # B. MRPC (News articles - Formal)
    print("Loading MRPC...")
    mrpc = load_dataset("glue", "mrpc", split="train")
    for row in mrpc:
        train_examples.append(InputExample(texts=[row['sentence1'], row['sentence2']], label=float(row['label'])))

    # C. STS Benchmark (Graded similarity)
    print("Loading STS-B...")
    stsb = load_dataset("glue", "stsb", split="train")
    for row in stsb:
        # Normalize 0-5 score to 0-1
        train_examples.append(InputExample(texts=[row['sentence1'], row['sentence2']], label=row['label'] / 5.0))

    # D. PAWS (Adversarial word-swaps)
    print("Loading PAWS...")
    try:
        paws = load_dataset("paws", "labeled_final", split="train[:10000]")
        for row in paws:
            train_examples.append(InputExample(texts=[row['sentence1'], row['sentence2']], label=float(row['label'])))
    except Exception as e:
        print(f"Skipping PAWS: {e}")

    # E. MNLI (Negation/Logic)
    print("Loading MNLI...")
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

    print(f"Total training examples: {len(train_examples)}")
    random.shuffle(train_examples)

    # 3. Training Configuration
    # Reduced batch size to 8 to avoid OOM on Mac 16GB
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=8)
    
    # We use ContrastiveLoss which handles both 0/1 labels and continuous labels well
    train_loss = losses.ContrastiveLoss(model=model)

    # 4. Run Training
    print("Starting Multi-Task Fine-Tuning...")
    
    # Set memory environment variable for MPS
    os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

    try:
        model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=1,
            warmup_steps=1000, 
            weight_decay=0.01,
            show_progress_bar=True
        )
    except Exception as e:
        print(f"CRITICAL: Training interrupted by error: {e}")
        print("Attempting emergency save of current weights...")
    
    # 5. Save the final model
    base_path = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_path, 'models', 'saved_model_v2')
    print(f"Saving Universal model to {output_path}...")
    model.save(output_path)
    print("Multi-Task Training completed.")

if __name__ == "__main__":
    train_multi_task_model()
