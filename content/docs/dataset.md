# Dataset Collection

## 1. Record

Set up the ports and cameras first, as in Camera Setup. Then record five episodes of one task:

```bash
lerobot-record \
    --robot.type=seeed_b601_rs_follower \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.can_adapter=socketcan \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
    --teleop.type=rebot_arm_102_leader \
    --teleop.port=/dev/ttyUSB0 \
    --teleop.id=rebot_arm_102_leader \
    --display_data=true \
    --dataset.repo_id=seeed_rebot_b601_rs/test \
    --dataset.num_episodes=5 \
    --dataset.single_task="Grab the black cube" \
    --dataset.push_to_hub=false \
    --dataset.episode_time_s=30 \
    --dataset.reset_time_s=30
```

`repo_id` is any name you like. The dataset is saved under `~/.cache/huggingface/lerobot/`.

Keys while recording:

- **Right arrow**: end the episode (or the reset) early and move on.
- **Left arrow**: cancel the episode and record it again.
- **Esc**: stop, encode the videos and finish.

To continue an interrupted recording, run the same command with `--resume=true`, with `--dataset.num_episodes` set to how many more episodes to add.

> [!TIP]
> Keep the cameras fixed, grasp the same way every time, and keep the object in view. Aim for 50 or more episodes. You should be able to do the task yourself from the camera images alone.

## 2. Visualize

```bash
lerobot-dataset-viz \
    --repo-id seeed_rebot_b601_rs/test \
    --episode-index 0 \
    --display-compressed-images=false
```

## 3. Replay

The robot repeats the first episode:

```bash
lerobot-replay \
    --robot.type=seeed_b601_rs_follower \
    --robot.port=can0 \
    --robot.can_adapter=socketcan \
    --robot.id=follower1 \
    --dataset.repo_id=seeed_rebot_b601_rs/test \
    --dataset.episode=0
```
