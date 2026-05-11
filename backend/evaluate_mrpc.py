import os
import torch
from datasets import load_dataset
from inference.predict import initialize_models, predict_similarity
from sklearn.metrics import accuracy_score, f1_score, classification_report
import numpy as np
from tqdm import tqdm

def evaluate_mrpc():
    print("\n" + "="*50)
    print("      Evaluating Model on MRPC Dataset      ")
    print("="*50)

    # 1. Initialize our Hybrid models
    initialize_models()

    # 2. Load MRPC validation set
    print("Loading MRPC validation dataset...")
    try:
        dataset = load_dataset("glue", "mrpc", split="validation")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    texts1 = dataset['sentence1']
    texts2 = dataset['sentence2']
    labels = dataset['label'] # 1 = paraphrase, 0 = not paraphrase

    print(f"Testing on {len(labels)} pairs...\n")

    predictions = []
    scores = []

    # 3. Run inference
    for t1, t2 in tqdm(zip(texts1, texts2), total=len(labels)):
        score, is_para = predict_similarity(t1, t2)
        predictions.append(1 if is_para else 0)
        scores.append(score)

    # 4. Compute Metrics
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions)
    
    print("\n" + "-"*30)
    print(f"ACCURACY: {acc:.4f} ({(acc*100):.2f}%)")
    print(f"F1 SCORE: {f1:.4f}")
    print("-"*30)
    
    print("\nDetailed Classification Report:")
    print(classification_report(labels, predictions, target_names=["Not Paraphrase", "Paraphrase"]))
    print("="*50 + "\n")

if __name__ == "__main__":
    evaluate_mrpc()
