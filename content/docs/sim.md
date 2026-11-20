# Sim to Real

Teleoperate a simulated reBot Arm in Isaac Sim with the real leader arm, record a LeRobot dataset there, and train on it as in Training and Evaluation. From Seeed's [rebot-arm-dli-isaacsim](https://github.com/Seeed-Projects/rebot-arm-dli-isaacsim) project.

Needs an NVIDIA RTX GPU with at least 12 GB of VRAM, Isaac Sim 6.1, and the calibrated leader arm.

## 1. Isaac Sim

Download the standalone Linux build from [NVIDIA](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/quick-install.html), then:

```bash
unzip isaac-sim-standalone-6.1.0-linux-x86_64.zip -d ~/isaacsim
cd ~/isaacsim
./post_install.sh
```

## 2. The Project

```bash
sudo apt install -y git-lfs
cd ~
git clone https://github.com/Seeed-Projects/rebot-arm-dli-isaacsim.git
cd rebot-arm-dli-isaacsim
git lfs install
git lfs pull
```

## 3. Teleoperate in the Simulation

```bash
cd ~/rebot-arm-dli-isaacsim
./run.sh --leader-port /dev/ttyUSB0
```

Click the Isaac Sim viewport first so it has keyboard focus. Keys while recording:

- **S**: start or stop an episode.
- **C**: discard the episode.

Episodes are saved as a LeRobot dataset in `datasets/rebot_stationery_front_side`.

## 4. Visualize and Replay

```bash
lerobot-dataset-viz \
    --repo-id local/rebot_stationery_front_side \
    --root ~/rebot-arm-dli-isaacsim/datasets/rebot_stationery_front_side \
    --episode-index 0
```

```bash
cd ~/rebot-arm-dli-isaacsim
./run.sh --no-start-bridge --no-recording --no-dr
~/rebot_lerobot/lerobot/.venv/bin/python scripts/replay_episode.py --episode 0
```
