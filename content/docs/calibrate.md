# Robot Calibration

> [!NOTE]
> These names are for the current Seeed fork of LeRobot, which has the reBot arm built in. Seeed's wiki uses an older setup with two plugin packages, where the follower is `seeed_b601_rs_follower` with `--robot.can_adapter=socketcan` and the leader is `rebot_arm_102_leader`. Use whichever your install knows: `lerobot-calibrate --help` lists the types.

## 1. Follower Arm

```bash
# Bring up the CAN interface
sudo ip link set can0 down 2>/dev/null
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up

# Calibrate
lerobot-calibrate \
    --robot.type=rebot_b601_follower \
    --robot.motor_family=rs \
    --robot.port=can0 \
    --robot.id=follower1
```

## 2. Leader Arm

```bash
# If the last line shows ttyUSB as "disconnected", remove brltty
sudo dmesg | grep ttyUSB
sudo apt remove brltty

# Grant access to the serial port
sudo chmod 666 /dev/ttyUSB0

# Calibrate
lerobot-calibrate \
    --teleop.type=rebot_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=leader1
```
