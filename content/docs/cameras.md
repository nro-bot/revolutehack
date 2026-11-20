# Camera Setup

## 1. Find the Cameras

```bash
# Intel RealSense: use realsense instead of opencv
lerobot-find-cameras opencv
```

Each camera's `Id` is its `index_or_path`. A test image from each camera is saved to `outputs/captured_images` in the current directory.

## 2. Teleoperate with One Camera

```bash
lerobot-teleoperate \
    --robot.type=rebot_b601_follower \
    --robot.motor_family=rs \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
    --teleop.type=rebot_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=leader1 \
    --display_data=true
```

## 3. Teleoperate with Two Cameras

```bash
lerobot-teleoperate \
    --robot.type=rebot_b601_follower \
    --robot.motor_family=rs \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
    --teleop.type=rebot_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=leader1 \
    --display_data=true
```

## Resources

- [Add Cameras](https://wiki.seeedstudio.com/rebot_arm_b601_rs_lerobot/#add-cameras), Seeed wiki
- [Cameras guide](https://github.com/Seeed-Projects/lerobot/blob/main/docs/source/cameras.mdx), Seeed LeRobot repository
- [Cameras](https://huggingface.co/docs/lerobot/cameras), LeRobot docs
