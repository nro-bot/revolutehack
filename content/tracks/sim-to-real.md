# Sim to Real

Teleoperate the reBot arm inside Isaac Sim, record LeRobot datasets there, train an imitation policy, then run it on the real arm with the real cameras. Sim data is cheap and unlimited; the question is whether the policy survives the gap in visuals, dynamics and calibration.

A weekend goal: one simple pick-and-place, 50 to 100 sim episodes with domain randomization, an ACT policy that works in sim, then a measured success rate on the real arm. Stretch: co-train with 10 to 20 real episodes and compare.

## Start here

- [rebot-arm-dli-isaacsim](https://github.com/Seeed-Projects/rebot-arm-dli-isaacsim): Seeed's Isaac Sim project for this arm. Leader-arm teleop of the simulated arm, LeRobot dataset recording, domain randomization of object pose, mass and lighting. See the Sim to Real tutorial step.
- [Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac](https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/): NVIDIA's free course. Sim data collection, domain randomization, co-training with real data, measuring the actuation gap. The steps map closely to the reBot workflow.
- [Sim-to-Real-SO-101-Workshop](https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop): the course's code, with evaluation scripts worth copying.
- [LeRobot: ACT](https://huggingface.co/docs/lerobot/act): training and deploying ACT on a real follower arm.
- [LeRobot: imitation learning in sim](https://huggingface.co/docs/lerobot/main/en/il_sim): the record, train, evaluate loop in MuJoCo, if Isaac Sim is too heavy for your machine.

## Papers

- [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705) (Zhao et al., 2023): introduces ACT. 50 demonstrations can be enough for contact-rich tasks.
- [Diffusion Policy](https://arxiv.org/abs/2303.04137) (Chi et al., 2023): the main alternative to ACT in LeRobot. Handles demonstrations that solve the task in several different ways.
- [Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907) (Tobin et al., 2017): why randomizing textures, lighting and camera pose makes a sim-trained vision model transfer.

## Tips

- One task, one object, a fixed start region. Match the real scene to the sim scene first: same camera placement and resolution, same table colour.
- Before training, check that joint order, units and calibration agree between the sim dataset and the real arm: replay a sim episode on the real arm with `lerobot-replay`.
- Measure success rate over 10 to 20 real trials per policy, the sim success rate of the same checkpoint, and the per-joint error when replaying a sim trajectory on the real arm.
