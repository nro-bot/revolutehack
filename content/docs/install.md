# LeRobot Installation

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

## 3A. Install with conda

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

Driver older than 580 only: the CUDA 12 build of PyTorch (stays on torch 2.14).

```bash
pip install --index-url https://download.pytorch.org/whl/cu126 torch torchvision
pip install --index-url https://download.pytorch.org/whl/cpu torchcodec
```

```bash
# Install LeRobot
cd ~/rebot_lerobot/lerobot
pip install -e ".[all]"
```

## 3B. Install with uv

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

Driver older than 580 only: the CUDA 12 build of PyTorch (stays on torch 2.14).

```bash
uv pip install --torch-backend cu126 torch torchvision
uv pip install --index-url https://download.pytorch.org/whl/cpu torchcodec
```

```bash
# Install LeRobot
uv pip install -e ".[all]"
```

> [!NOTE]
> The reBot arm is built into this fork, so no extra plugin packages are needed.
