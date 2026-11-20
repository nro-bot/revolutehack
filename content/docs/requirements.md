# Requirements

Ubuntu 22.04 or 24.04, Python 3.12 or newer, and ffmpeg. An NVIDIA GPU is optional: training needs it, the rest runs on the CPU.

## 1. System Packages

```bash
sudo apt update && sudo apt install -y git curl ffmpeg
```

## 2. NVIDIA Driver

PyTorch's default build needs driver 580.65 or newer. Check yours:

```bash
nvidia-smi --query-gpu=driver_version --format=csv,noheader
```

If it is older, update the driver and reboot:

```bash
sudo apt install -y nvidia-driver-580-open
sudo reboot
```

Or keep the old driver and install the CUDA 12 build of PyTorch before LeRobot (this stays on torch 2.14):

```bash
uv pip install --torch-backend cu126 torch torchvision
uv pip install --index-url https://download.pytorch.org/whl/cpu torchcodec
```
