# Gravity Compensation

Make the arm weightless: each joint is commanded the torque that gravity exerts on the links beyond it, so the motors hold the arm's weight and a person moving it by hand feels only friction and inertia. The RobStride motors make this feasible. They are backdrivable and torque-controllable in MIT mode, where each command carries a position, a velocity, gains and a feed-forward torque.

A weekend goal: compute the gravity torque from the arm's URDF with Pinocchio, send it as the feed-forward torque with near-zero gains, measure a per-joint scale and friction, tune, and demo a floating arm. Stretch: learn a residual torque model from logged pose and torque data, or build kinesthetic teaching on top, moving the arm by hand to record demonstrations.

## Start here

- [Seeed's gravity compensation demo](https://www.youtube.com/watch?v=qOhz4Im6hcM): what the finished thing looks like.
- [gravity.py in Seeed's LeRobot plugin](https://github.com/Seeed-Projects/lerobot-robot-seeed-b601/blob/main/lerobot_robot_seeed_b601/gravity.py): a working gravity feed-forward from the URDF, wired into the MIT command. The tutorial's install step puts this plugin in your environment. Its [URDF](https://github.com/Seeed-Projects/lerobot-robot-seeed-b601/blob/main/lerobot_robot_seeed_b601/assets/00-arm-rs_asm-v3.urdf) is the mass model.
- [Seeed's Pinocchio guide](https://wiki.seeedstudio.com/rebot_arm_b601_rs_pinocchio_meshcat/): computing the gravity torque and sending it, with the gains Seeed uses.
- [Seeed's RS identification write-up](https://github.com/Seeed-Projects/reBotArm_control_py/blob/main/docs/gravity_calibration_rs_2026-07-17.md): measured scale factors, friction and pitfalls on this exact arm, with the [measurement harness](https://github.com/Seeed-Projects/reBotArm_control_py/blob/main/tools/gravity_calibration/README.md).
- [RobStride motor control](https://wiki.seeedstudio.com/robstride_control/): MIT mode, gain ranges per motor, CAN IDs, error codes.
- [Pinocchio inverse dynamics example](https://github.com/stack-of-tasks/pinocchio/blob/master/examples/inverse-dynamics.py): gravity torque from a URDF in a few lines.

## References

- [Dynamic identification of the Franka Emika Panda robot with retrieval of feasible parameters](https://iris.uniroma1.it/bitstream/11573/1356777/2/Gaz_Postprint_Dynamic-Identification_2019.pdf) (Gaz et al., 2019): identifying masses and friction from data.
- [Zero-force drag and start-up torque compensation strategies for robots](https://www.cambridge.org/core/journals/robotica/article/zeroforce-drag-and-startup-torque-compensation-strategies-for-robots/66BBC748206D3F79F3E8BD4C51147E7B) (Li et al., 2025): gravity plus friction from joint currents.
- [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics), chapter 8, Dynamics of Open Chains: the theory, free.

## Tips

- Joints 2 and 3 carry nearly all the gravity load; the wrist's gravity torque is below its friction. Start one joint at a time, fit a scale and a friction term per joint, then add a small gain or a friction term to cover the floor of a few tenths of a newton-metre.
- Identify from poses with clearance; contact with the table or another link produces convincing fake fits. Compute velocity by differencing positions. Log motor temperature: holding torque heats the wrist motors.
- Never cut torque on a raised arm, it falls. Ramp the feed-forward in over a second or two, abort into a position hold, clamp the torque to a fraction of peak, and keep the workspace clear.
- Measure the holding error per joint across poses, and how much force it takes to move the arm by hand, before and after.
