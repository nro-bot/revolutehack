# Object Tracking

Detect an object in the camera and make the arm follow it: keep it centred in the image, then reach to it. The simplest loop skips camera-to-robot calibration altogether. Measure the pixel error between the object and the image centre, turn it into small joint increments (base yaw from the x error, shoulder or wrist pitch from the y error), and send them at 10 to 30 Hz with a low gain and a dead band.

A weekend plan: day one, frames from the camera and a detector, then the centring loop. Day two, a fixed-camera variant where a marker pose or RealSense depth gives a 3D target. Stretch: reach and grasp, which needs eye-in-hand calibration.

## Start here

- [Ultralytics YOLO, tracking mode](https://docs.ultralytics.com/modes/track/): detection with persistent object IDs, a few lines of Python.
- [OpenCV ArUco detection](https://github.com/opencv/opencv/blob/4.x/doc/tutorials/objdetect/aruco_detection/aruco_detection.markdown): a printed marker gives a full 3D pose with no training. The safest starting point.
- [SAM 2](https://github.com/facebookresearch/sam2): click an object once and its video predictor tracks the mask through frames.
- [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO): detect "red cup" from a text prompt.
- [ViSP image-based visual servoing](https://visp-doc.inria.fr/doxygen/visp-daily/tutorial-ibvs.html) and [eye-in-hand calibration](https://visp-doc.inria.fr/doxygen/visp-daily/tutorial-calibration-extrinsic-eye-in-hand.html): the theory and a library, for the reach-to-it stretch.
- [LeRobot cameras](https://huggingface.co/docs/lerobot/cameras): reading frames, `read_latest`, RealSense depth.
- [RebotB601Follower](https://github.com/Seeed-Projects/lerobot/blob/main/src/lerobot/robots/rebot_b601_follower/rebot_b601_follower.py): `get_observation()` and `send_action()` with per-joint position targets, clipped by `max_relative_target` and the soft joint limits.

## Papers

- [SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714) (Ravi et al., 2024)
- [Grounding DINO](https://arxiv.org/abs/2303.05499) (Liu et al., 2023): open-set object detection from text.
- [ViT-VS](https://arxiv.org/abs/2503.04545) (Scherl et al., 2025): visual servoing on pretrained vision transformer features.

## Tips

- "Keep the object centred" is a complete demo; "reach to it" is the stretch. Use a bright, distinct object, with a colour threshold as the fallback if the detector fails.
- Detector time plus camera buffering is often 100 ms or more. Servo on the newest frame with `read_latest`, run the detector at 640 by 480 or smaller, smooth the target with a moving average, and cap the per-step joint change with `max_relative_target` so one bad detection cannot throw the arm.
- Keep the soft joint limits on and Ctrl-C ready. Start with the gripper and wrist away from the table.
- Measure pixel error over time, settling time after moving the object, and the loop rate in Hz. Those three make a convincing final plot.
