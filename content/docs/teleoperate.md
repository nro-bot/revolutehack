# Teleoperation

> [!CAUTION]
> If either arm loses power or a signal cable comes loose, stop the program and return both arms to their zero position **before** reconnecting power and restarting. Otherwise the arm can run away.

## 1. Set Up Ports

```bash
# Leader
sudo chmod 666 /dev/ttyUSB*

# Follower
sudo ip link set can0 down 2>/dev/null
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
```

## 2. Teleoperate

```bash
lerobot-teleoperate \
    --robot.type=seeed_b601_rs_follower \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.can_adapter=socketcan \
    --teleop.type=rebot_arm_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=rebot_arm_102_leader
```
