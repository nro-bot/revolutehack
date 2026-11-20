# About

## What is a reBot Arm?

The reBot Arm B601-RS is a six-joint robot arm made by Seeed, launched as an open-source arm to lower the barrier to learning embodied intelligence.

## What is LeRobot?

LeRobot is Hugging Face's open-source robot learning library, written in PyTorch. It focuses on imitation learning and reinforcement learning, and provides pretrained models, datasets of human demonstrations, and simulation environments.

## Teleoperate, record, train

1. You move the leader arm by hand, and the follower copies it in real time.
2. While you do that, cameras and joint positions are recorded as episodes. One episode is one attempt at the task, like "grab the black cube".
3. You train a neural network on those episodes.
4. The trained network then looks through the cameras and moves the arm by itself.

## What you need

- Ubuntu 22.04 or 24.04
- Python 3.12 or newer
- PyTorch 2.7 to 2.15, installed for you. The default build needs NVIDIA driver 580.65 or newer; an older driver can use the CUDA 12 build, which stops at torch 2.14.
- An NVIDIA GPU, optional. Teleoperation and recording run on the CPU; training needs the GPU.

## Specifications

| Item | Spec |
| --- | --- |
| Degrees of freedom | 6 + 1 (gripper) |
| Reach | 754.7 mm with gripper, 587.5 mm without |
| Payload | 2.5 kg rated, 5 kg max |
| Repeatability | 0.1 mm |
| Weight | 6.7 kg |
| Motors | 3 RobStride 06, 4 RobStride 00 |
| Communication | CAN bus at 1 Mbps |
| Operating voltage | DC 48 V |
| Power supply | DC 48 V, 15 A |

## Safety

> [!CAUTION]
> Stay aware of your surroundings and confirm the area is clear before operating any robot arm. Keep hands, loose clothing and accessories clear of moving parts, and never leave a powered arm unattended. Cut power immediately if anything behaves unexpectedly.

- Handle all hardware with care.
- Respect other participants' workspaces and equipment, and ask before handling anything that is not yours.
- Return all tools and materials to their designated place before leaving.
