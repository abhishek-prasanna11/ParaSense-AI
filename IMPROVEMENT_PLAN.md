# Implementation Plan - Phase 2: Further Improvement (Universal Performance)

The current model has achieved 100% accuracy on negation traps and ~70% on news data (MRPC). To reach the next level (>85% universal accuracy), we must move to a Multi-Task Training approach.

## Goals
1.  **Universal Accuracy**: Increase MRPC and general domain performance from 70% to 85%+.
2.  **Domain Versatility**: Ensure the model works equally well on questions, news, and informal chats.
3.  **Knowledge Distillation**: Use a large "Teacher" model to guide the smaller "Student" (MPNet).

## Proposed Changes

### 1. Multi-Task Data Pipeline (`backend/models/transformer_model_v2.py`)
- [NEW] Implement a data loader that blends:
    - **QQP** (30k rows) - For conversational similarity.
    - **MRPC** (4k rows) - For formal/news similarity.
    - **STS-B** (5k rows) - For graded semantic distance.
    - **PAWS** (10k rows) - To maintain the fix for adversarial word-swaps.
    - **MNLI** (10k rows) - To maintain the fix for negation logic.

### 2. Training Strategy: Knowledge Distillation
- Use a **Cross-Encoder Teacher** (`cross-encoder/stsb-roberta-large`) to generate "soft labels" for the training pairs.
- Instead of just training on 0 or 1, the model will learn to predict the exact nuance captured by the large RoBERTa model.

### 3. Hyperparameter Optimization
- **CosineAnnealingLR**: Use a more sophisticated learning rate scheduler to prevent overfitting to any single dataset in the mix.
- **Gradient Accumulation**: Increase effective batch size to 64 for more stable updates on complex data.

## Verification Plan

### Automated Benchmarks
- Run `evaluate_mrpc.py` -> **Target: >80%**.
- Run `test_50_examples.py` -> **Target: 100% (No regressions)**.
- [NEW] Evaluate on **STS-Benchmark** test set -> **Target: Spearman Correlation > 0.85**.

### Manual Verification
- Test complex idioms and metaphors in the UI (e.g., "The ball is in your court" vs "It is up to you").
