import torch

def get_device():
    """
    Returns the best available PyTorch device.
    Supports CUDA (Windows/Linux NVIDIA GPUs),
    MPS (Mac M-series chips), and CPU.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")
