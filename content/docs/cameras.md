# Camera Setup

## 1. Find the Cameras

```bash
# Intel RealSense: use realsense instead of opencv
lerobot-find-cameras opencv
```

This lists every camera, including a laptop's built-in webcam, and saves a test image from each to `outputs/captured_images`.

Which camera is which, by name. A camera's Id is the number of the first `/dev/videoN` under it; the USB camera is usually not 0.

```bash
sudo apt install -y v4l-utils
v4l2-ctl --list-devices

# Watch one live
ffplay -f v4l2 /dev/video0
```

## 2. Teleoperate with One Camera

```bash
# index_or_path is the camera's Id from step 1.
# Image upside down: rotation: 180.
lerobot-teleoperate \
    --robot.type=rebot_b601_follower \
    --robot.motor_family=rs \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: MJPG, rotation: 0}}" \
    --teleop.type=rebot_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=leader1 \
    --display_data=true
```

## 3. Teleoperate with Two Cameras

```bash
# One index_or_path per camera, from step 1.
lerobot-teleoperate \
    --robot.type=rebot_b601_follower \
    --robot.motor_family=rs \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: MJPG, rotation: 0}, side: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30, fourcc: MJPG, rotation: 0}}" \
    --teleop.type=rebot_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=leader1 \
    --display_data=true
```

## Resources

- [Add Cameras](https://wiki.seeedstudio.com/rebot_arm_b601_rs_lerobot/#add-cameras), Seeed wiki
- [Cameras guide](https://github.com/Seeed-Projects/lerobot/blob/main/docs/source/cameras.mdx), Seeed LeRobot repository
- [Cameras](https://huggingface.co/docs/lerobot/cameras), LeRobot docs
