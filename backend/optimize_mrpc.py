import os
from datasets import load_dataset
from inference import predict as inference
from sentence_transformers import util
import numpy as np
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score

def optimize_thresholds():
    print("\n" + "="*50)
    print("      Optimizing Thresholds for MRPC      ")
    print("="*50)

    inference.initialize_models()

    print("Loading MRPC validation dataset...")
    dataset = load_dataset("glue", "mrpc", split="validation")
    texts1, texts2, labels = dataset['sentence1'], dataset['sentence2'], dataset['label']

    print("Extracting raw scores from Bi-Encoder and Cross-Encoder...")
    bi_scores = []
    cross_scores = []

    for t1, t2 in tqdm(zip(texts1, texts2), total=len(labels)):
        # 1. Bi-Encoder Score
        emb1 = inference._bi_model.encode(t1, convert_to_tensor=True)
        emb2 = inference._bi_model.encode(t2, convert_to_tensor=True)
        bi_scores.append(util.cos_sim(emb1, emb2).item())

        # 2. Cross-Encoder Score
        cross_scores.append(inference._cross_model.predict([t1, t2]))

    bi_scores = np.array(bi_scores)
    cross_scores = np.array(cross_scores)
    labels = np.array(labels)

    # Grid Search
    best_acc = 0
    best_bi_thresh = 0
    best_cross_thresh = 0

    print("\nSearching for optimal thresholds...")
    for bi_thresh in np.arange(0.5, 0.85, 0.05):
        for cross_thresh in np.arange(0.1, 0.9, 0.05):
            preds = []
            for b, c in zip(bi_scores, cross_scores):
                if b > 0.65:
                    preds.append(1 if (b > bi_thresh and c > cross_thresh) else 0)
                else:
                    preds.append(1 if b > bi_thresh else 0)
            
            acc = accuracy_score(labels, preds)
            if acc > best_acc:
                best_acc = acc
                best_bi_thresh = bi_thresh
                best_cross_thresh = cross_thresh

    print("\n" + "-"*30)
    print(f"OPTIMAL BI-THRESHOLD   : {best_bi_thresh:.2f}")
    print(f"OPTIMAL CROSS-THRESHOLD: {best_cross_thresh:.2f}")
    print(f"MAX ACCURACY ACHIEVED  : {best_acc:.4f} ({(best_acc*100):.2f}%)")
    print("-"*30 + "\n")

if __name__ == "__main__":
    optimize_thresholds()
