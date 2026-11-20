# Conda

## 1. System Packages

```bash
sudo apt update && sudo apt install -y git curl
```

## 2. Clone LeRobot

```bash
mkdir -p ~/rebot_lerobot
cd ~/rebot_lerobot
git clone https://github.com/Seeed-Projects/lerobot.git
```

## 3. Install

```bash
# Install Miniforge
cd ~
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
~/miniforge3/bin/conda init bash
source ~/.bashrc

# Create and activate the environment
conda create -y -n lerobot python=3.12
conda activate lerobot

# Install ffmpeg (if video errors occur, use ffmpeg=7.1.1 instead)
conda install -y ffmpeg -c conda-forge
```

### NVIDIA GPU (optional)

Check the driver version. Older than 580: install PyTorch for CUDA 12 first.

```bash
nvidia-smi --query-gpu=driver_version --format=csv,noheader
```

```bash
pip install --index-url https://download.pytorch.org/whl/cu126 torch torchvision
pip install --index-url https://download.pytorch.org/whl/cpu torchcodec
```

### Install LeRobot

```bash
# Install LeRobot and the Seeed plugins
cd ~/rebot_lerobot/lerobot
pip install -e ".[all]"
pip install lerobot-robot-seeed-b601 lerobot-teleoperator-rebot-arm-102
```
