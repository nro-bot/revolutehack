# Calibration

## 1. Follower Arm

```bash
# Bring up the CAN interface
sudo ip link set can0 down 2>/dev/null
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up

# Calibrate
lerobot-calibrate \
    --robot.type=seeed_b601_rs_follower \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.can_adapter=socketcan
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
    --teleop.type=rebot_arm_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=rebot_arm_102_leader
```
