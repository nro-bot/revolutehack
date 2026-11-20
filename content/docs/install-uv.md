# UV

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
# Install uv and ffmpeg
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
sudo apt install -y ffmpeg

# Create and activate the environment
cd ~/rebot_lerobot/lerobot
uv venv --python 3.12
source .venv/bin/activate
```

NVIDIA driver older than 580: install PyTorch for CUDA 12 first.

```bash
uv pip install --torch-backend cu126 torch torchvision
uv pip install --index-url https://download.pytorch.org/whl/cpu torchcodec
```

```bash
# Install LeRobot and the Seeed plugins
uv pip install -e ".[all]"
uv pip install lerobot-robot-seeed-b601 lerobot-teleoperator-rebot-arm-102
```
