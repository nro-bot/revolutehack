# Requirements

Ubuntu 22.04 or 24.04, Python 3.12 or newer, ffmpeg. NVIDIA GPU optional: needed for training only.

## 1. System Packages

```bash
sudo apt update && sudo apt install -y git curl ffmpeg
```

## 2. NVIDIA Driver

PyTorch's default build: driver 580.65 or newer.

```bash
# Check the driver version
nvidia-smi --query-gpu=driver_version --format=csv,noheader
```

### 2A. Driver older than 580: update it

```bash
sudo apt install -y nvidia-driver-580-open
sudo reboot
```

### 2B. Driver older than 580: keep it, use the CUDA 12 build of PyTorch

Run before installing LeRobot. Stays on torch 2.14.

```bash
uv pip install --torch-backend cu126 torch torchvision
uv pip install --index-url https://download.pytorch.org/whl/cpu torchcodec
```
