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

# Install LeRobot and the Seeed plugins
cd ~/rebot_lerobot/lerobot
pip install -e ".[all]"
pip install lerobot-robot-seeed-b601 lerobot-teleoperator-rebot-arm-102

# Activate environment
conda activate lerobot
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

# Install LeRobot and the Seeed plugins
uv pip install -e ".[all]"
uv pip install lerobot-robot-seeed-b601 lerobot-teleoperator-rebot-arm-102

# Activate environment
source .venv/bin/activate
```
