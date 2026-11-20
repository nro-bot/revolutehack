# Camera Setup

## 1. Find the Cameras

```bash
# Intel RealSense: use realsense instead of opencv
lerobot-find-cameras opencv
```

This lists every camera, including a laptop's built-in webcam. Each camera's `Id` is its `index_or_path`, and a test image from each is saved to `outputs/captured_images`. Open the images to see which `Id` is the USB camera on the robot, usually not `0`, and use that `Id` below.

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

`index_or_path: 0` is the USB camera's `Id` from step 1.

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
