# Training and Evaluation

## 1. Train

Train an ACT policy on the dataset you recorded. Use the same `repo_id` as when recording.

```bash
lerobot-train \
    --dataset.repo_id=seeed_rebot_b601_rs/test \
    --policy.type=act \
    --policy.push_to_hub=false \
    --output_dir=outputs/train/act_rebot_test \
    --job_name=act_rebot_test \
    --policy.device=cuda \
    --wandb.enable=false \
    --steps=300000
```

Checkpoints are saved under `outputs/train/act_rebot_test/checkpoints/`, so you can stop early and evaluate the latest one.

> [!NOTE]
> Training needs an NVIDIA GPU. 50 episodes take about 6 hours on an RTX 3060, and 2 to 3 hours on an RTX 4090.

## 2. Evaluate

Run the policy on the robot. This records 10 episodes of the policy's own attempts, with the same cameras as the dataset.

```bash
lerobot-record \
    --robot.type=rebot_b601_follower \
    --robot.motor_family=rs \
    --robot.port=can0 \
    --robot.id=follower1 \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: MJPG, rotation: 0}, side: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30, fourcc: MJPG, rotation: 0}}" \
    --display_data=false \
    --dataset.repo_id=seeed_rebot_b601_rs/eval_test \
    --dataset.single_task="Grab the black cube" \
    --dataset.num_episodes=10 \
    --dataset.push_to_hub=false \
    --policy.path=outputs/train/act_rebot_test/checkpoints/last/pretrained_model
```

If you see `mean is infinity`, the camera names (`front`, `side`) do not match the ones used when recording.
