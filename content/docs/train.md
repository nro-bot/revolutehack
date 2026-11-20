# Training and Evaluation

## 1. Train

Train a policy on the dataset you recorded. ACT is the quick one; the others are larger pretrained models that need more GPU memory and time. More models and options: [Seeed's wiki](https://wiki.seeedstudio.com/rebot_arm_b601_rs_lerobot/#training-and-evaluation).

<!-- tabs -->
### ACT

```bash
lerobot-train \
    --dataset.repo_id=seeed_rebot_b601_rs/test \
    --policy.type=act \
    --policy.push_to_hub=false \
    --output_dir=outputs/train/act_rebot_test \
    --job_name=act_rebot_test \
    --policy.device=cuda \
    --steps=300000
```

### SmolVLA

Fine-tunes the pretrained `smolvla_base`. Lower `batch_size` first if the GPU runs out of memory.

```bash
uv pip install -e ".[smolvla]"
```

```bash
lerobot-train \
    --policy.path=lerobot/smolvla_base \
    --dataset.repo_id=seeed_rebot_b601_rs/test \
    --policy.push_to_hub=false \
    --output_dir=outputs/train/smolvla_rebot_test \
    --job_name=smolvla_rebot_test \
    --policy.device=cuda \
    --batch_size=64 \
    --steps=20000
```

### Pi0

Fine-tunes the pretrained `pi0_base`, in bfloat16 with gradient checkpointing to fit in memory.

```bash
uv pip install -e ".[pi]"
```

```bash
lerobot-train \
    --policy.type=pi0 \
    --policy.pretrained_path=lerobot/pi0_base \
    --dataset.repo_id=seeed_rebot_b601_rs/test \
    --policy.push_to_hub=false \
    --output_dir=outputs/train/pi0_rebot_test \
    --job_name=pi0_rebot_test \
    --policy.device=cuda \
    --policy.dtype=bfloat16 \
    --policy.gradient_checkpointing=true \
    --policy.compile_model=true \
    --batch_size=32 \
    --steps=3000
```

### Pi0.5

Same as Pi0, with the newer `pi05_base`.

```bash
uv pip install -e ".[pi]"
```

```bash
lerobot-train \
    --policy.type=pi05 \
    --policy.pretrained_path=lerobot/pi05_base \
    --dataset.repo_id=seeed_rebot_b601_rs/test \
    --policy.push_to_hub=false \
    --output_dir=outputs/train/pi05_rebot_test \
    --job_name=pi05_rebot_test \
    --policy.device=cuda \
    --policy.dtype=bfloat16 \
    --policy.gradient_checkpointing=true \
    --policy.compile_model=true \
    --batch_size=32 \
    --steps=3000
```
<!-- /tabs -->

Checkpoints are saved under the output folder's `checkpoints/`, so you can stop early and evaluate the latest one.

> [!NOTE]
> Training needs an NVIDIA GPU. ACT on 50 episodes takes about 6 hours on an RTX 3060, and 2 to 3 hours on an RTX 4090.

## 2. Evaluate

Run the policy on the robot. This records 10 episodes of the policy's own attempts, with the same cameras as the dataset.

<!-- tabs -->
### ACT

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
    --dataset.no_stamp=true \
    --policy.path=outputs/train/act_rebot_test/checkpoints/last/pretrained_model
```

### SmolVLA

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
    --dataset.no_stamp=true \
    --policy.path=outputs/train/smolvla_rebot_test/checkpoints/last/pretrained_model
```

### Pi0

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
    --dataset.no_stamp=true \
    --policy.path=outputs/train/pi0_rebot_test/checkpoints/last/pretrained_model
```

### Pi0.5

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
    --dataset.no_stamp=true \
    --policy.path=outputs/train/pi05_rebot_test/checkpoints/last/pretrained_model
```
<!-- /tabs -->

If you see `mean is infinity`, the camera names (`front`, `side`) do not match the ones used when recording.
