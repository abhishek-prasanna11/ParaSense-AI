# Setup Guide: Running the Paraphrase Detection Model

This guide explains how to set up the project on a new machine and download the fine-tuned model weights using Git LFS.

## 1. Clone & Switch Branch
First, clone the repository and switch to the branch containing the fine-tuned weights:
```bash
git clone https://github.com/dharani070707/paraphase_semantic_analysis.git
cd paraphase_semantic_analysis
git checkout feature/fine-tuned-model
```

## 2. Install & Pull Git LFS (Crucial)
The model weights are stored using **Git Large File Storage (LFS)**. You must have Git LFS installed or you will only download tiny pointer files instead of the actual weights.

### On macOS (Homebrew):
```bash
brew install git-lfs
git lfs install
git lfs pull
```

### On Windows/Linux:
Download the installer from [git-lfs.com](https://git-lfs.com/), then run:
```bash
git lfs install
git lfs pull
```

## 3. Set Up Python Environment
Navigate to the `backend` folder and install the dependencies:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Run the Test
Use the pre-configured test script to verify that the model is loading the fine-tuned MPNet weights correctly:

```bash
python test_examples.py
```

### Note on Hardware:
*   The code is optimized for **Apple Silicon (MPS)**.
*   If running on a standard CPU or Nvidia GPU, the code will automatically detect and use `cpu` or `cuda` via the `get_device()` utility in `models/device.py`.
