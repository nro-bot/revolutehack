# 3D Modeling

Teach the arm to look at an object from enough viewpoints to build a good 3D model of it. Mount the camera on the wrist, drive the arm through poses around a small object, capture an image at each stop, and reconstruct. The arm's kinematics plus a one-time hand-eye calibration give the camera pose for every frame, which is what usually fails on small, low-texture objects.

The smart part replaces a fixed orbit with next-best-view: after each batch, score candidate poses by how much unseen surface they would reveal, move to the best one, repeat. Compare against a fixed orbit with the same image budget.

## Start here

- [Nerfstudio](https://docs.nerf.studio/): nerfacto and splatfacto reconstruction from posed images.
- [COLMAP](https://colmap.github.io/): structure from motion and multi-view stereo, the classic photogrammetry pipeline.
- [Open3D reconstruction system](https://www.open3d.org/docs/latest/tutorial/reconstruction_system/index.html): fusing RGB-D frames from a RealSense.
- [pyrealsense2](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python): the RealSense Python wrapper.
- [Hand-eye calibration with OpenCV](https://roboflow.com/blog/hand-eye-calibration): finding the camera-to-gripper transform, step by step.
- [nbvplanner](https://github.com/ethz-asl/nbvplanner): a reference next-best-view planner.

## Papers

- [ActiveNeRF: Learning where to See with Uncertainty Estimation](https://arxiv.org/abs/2209.08546) (2022)
- [NeurAR: Neural Uncertainty for Autonomous 3D Reconstruction](https://arxiv.org/abs/2207.10985) (2022)
- [ActiveSplat: High-Fidelity Scene Reconstruction through Active Gaussian Splatting](https://arxiv.org/abs/2410.21955) (2024)
- [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/abs/2308.04079) (2023)

## Tips

- One textured object about 10 cm across, 30 to 60 views, a hemisphere only. Day one: calibration, pose list, capture script, a first reconstruction. Day two: the next-best-view loop, a greedy voxel-coverage planner is enough.
- Stop the arm and wait half a second before each capture to avoid motion blur. Fix exposure and white balance. A wrong camera-to-gripper transform silently ruins everything, so validate it by reprojecting a checkerboard. The D405 is a near-range camera: keep it within about 7 to 50 cm.
- Check which poses the arm can actually reach before planning over them.
- Measure with a known object: surface coverage per image count, Chamfer distance to the true mesh, PSNR on held-out views. Plot next-best-view against the fixed orbit at equal image budgets.
