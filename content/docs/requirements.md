# Requirements

Ubuntu 22.04 or 24.04, Python 3.12 or newer, ffmpeg. NVIDIA GPU optional: needed for training only.

## 1. System Packages

```bash
sudo apt update && sudo apt install -y git curl ffmpeg
```

## 2. NVIDIA Driver (optional)

PyTorch's default build: driver 580.65 or newer.

```bash
# Check the driver version
nvidia-smi --query-gpu=driver_version --format=csv,noheader
```

Driver older than 580: update it, or install the CUDA 12 build of PyTorch during the installation step.

```bash
# Remove the old driver first: its packages conflict with the new ones
sudo apt purge '*nvidia*570*'
sudo apt autoremove

sudo apt install -y nvidia-driver-580-open
sudo reboot
```
