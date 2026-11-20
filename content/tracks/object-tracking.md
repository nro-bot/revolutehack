# Object Tracking

Detect an object in the camera and move the arm to keep it centred, then reach to it. The simplest loop turns the object's pixel error into small joint moves, with no camera calibration.

## Links

- [Ultralytics YOLO, tracking mode](https://docs.ultralytics.com/modes/track/): detection with persistent IDs.
- [OpenCV ArUco](https://github.com/opencv/opencv/blob/4.x/doc/tutorials/objdetect/aruco_detection/aruco_detection.markdown): a printed marker gives a 3D pose with no training.
- [SAM 2](https://github.com/facebookresearch/sam2) and [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO): track a clicked object, or detect one from a text prompt.
- [ViSP visual servoing tutorial](https://visp-doc.inria.fr/doxygen/visp-daily/tutorial-ibvs.html): the theory, for reaching to the object.
- [RebotB601Follower](https://github.com/Seeed-Projects/lerobot/blob/main/src/lerobot/robots/rebot_b601_follower/rebot_b601_follower.py): sending joint targets from Python.

## Videos

- [Braccio arm pickup with OpenCV object detection](https://www.youtube.com/watch?v=y_R0t8rGT8o): detect, then reach.
- [Robot head tracking a ball with OpenCV](https://www.youtube.com/watch?v=gsktsIc4Fjs): the centring loop, with a colour detector.
- [Shadow Robot visual servoing](https://www.youtube.com/watch?v=CQOnBJyfvr8): a simulated arm following a real object.
