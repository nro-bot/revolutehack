# Robot Calibration

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

Press `c` to start the calibration.

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
