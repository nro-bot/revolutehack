# Gravity Compensation

Command each joint the torque that gravity puts on it, so the arm floats and can be moved by hand. The RobStride motors take a feed-forward torque in MIT mode, which makes this possible.

## Links

- [gravity.py in Seeed's LeRobot plugin](https://github.com/Seeed-Projects/lerobot-robot-seeed-b601/blob/main/lerobot_robot_seeed_b601/gravity.py): a working gravity feed-forward from the arm's [URDF](https://github.com/Seeed-Projects/lerobot-robot-seeed-b601/blob/main/lerobot_robot_seeed_b601/assets/00-arm-rs_asm-v3.urdf). The install step puts this plugin in your environment.
- [Seeed's Pinocchio guide](https://wiki.seeedstudio.com/rebot_arm_b601_rs_pinocchio_meshcat/): computing and sending the gravity torque.
- [Seeed's identification write-up](https://github.com/Seeed-Projects/reBotArm_control_py/blob/main/docs/gravity_calibration_rs_2026-07-17.md): measured scale and friction on this exact arm.
- [RobStride motor control](https://wiki.seeedstudio.com/robstride_control/): MIT mode, gain ranges, CAN IDs.
- [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics), chapter 8: the theory, free.

## Videos

- [reBot Arm B601-RS gravity compensation](https://www.youtube.com/watch?v=qOhz4Im6hcM): Seeed's demo on this arm.
- [GLUON robotic arm gravity compensation](https://www.youtube.com/watch?v=hVikkLC9sb0): the same effect on another arm.
- [S-drive gravity compensation mode](https://www.youtube.com/watch?v=TITTxwZSgXE): a minimal arm, the same idea.
