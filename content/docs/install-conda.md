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

Driver older than 580 only: the CUDA 12 build of PyTorch (stays on torch 2.14).

```bash
pip install --index-url https://download.pytorch.org/whl/cu126 torch torchvision
pip install --index-url https://download.pytorch.org/whl/cpu torchcodec
```

```bash
# Install LeRobot and the Seeed plugins
cd ~/rebot_lerobot/lerobot
pip install -e ".[all]"
pip install lerobot-robot-seeed-b601 lerobot-teleoperator-rebot-arm-102
```

The fork has the arm built in as `rebot_b601_follower` and `rebot_102_leader`; the plugins add the names Seeed's wiki uses, `seeed_b601_rs_follower` and `rebot_arm_102_leader`, so either set works.
