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
    --robot.type=rebot_b601_follower \
    --robot.motor_family=rs \
    --robot.port=can0 \
    --robot.id=follower1 \
    --teleop.type=rebot_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=leader1
```

Press `Ctrl` + `C` to stop.
