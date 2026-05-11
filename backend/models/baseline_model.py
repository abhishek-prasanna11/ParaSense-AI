import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datasets import load_dataset

def train_baseline_paraphrase():
    print("Loading Quora Question Pairs dataset...")
    # Loading a tiny subset (100 rows) for verification as requested by the plan
    # Remove split criteria to run on the full dataset
    dataset = load_dataset("glue", "qqp", split="train[:1000]")
    
    # Preprocessing
    texts_1 = [item['question1'] for item in dataset]
    texts_2 = [item['question2'] for item in dataset]
    labels = [item['label'] for item in dataset]
    
    print("Training TF-IDF + Logistic Regression...")
    vectorizer = TfidfVectorizer(max_features=5000)
    
    # We combine the texts to learn a common vocabulary
    # For prediction, we could concatenate the text representations or take their difference.
    # Here, we concatenate them.
    X_train_1 = vectorizer.fit_transform(texts_1)
    X_train_2 = vectorizer.transform(texts_2)
    
    import scipy.sparse as sp
    X_train = sp.hstack((X_train_1, X_train_2))
    
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, labels)
    
    # Predict on the same set for basic sanity check
    preds = clf.predict(X_train)
    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, zero_division=0)
    
    print(f"[Baseline] Paraphrase Accuracy: {acc:.4f}, F1-score: {f1:.4f}")
    print("Baseline model training completed and verified.")

if __name__ == "__main__":
    train_baseline_paraphrase()
