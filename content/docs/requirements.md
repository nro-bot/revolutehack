# Requirements

- Ubuntu 22.04 or 24.04. Linux is the documented platform for the arm.
- Python 3.12 or newer. The fork requires at least 3.12.
- PyTorch 2.7 up to 2.15. The installer picks it for you. The default Linux build is a CUDA 13 build and needs NVIDIA driver 580.65 or newer; with an older driver the install warns that the driver is too old. In that case install the CUDA 12 build of torch first, which tops out at torch 2.14.
- ffmpeg, as a system package with uv, or from conda-forge with conda.
- An NVIDIA GPU, optional. Calibration, teleoperation and recording run on the CPU. Training is where the GPU matters, roughly hours on an RTX 3060 versus days without one.
