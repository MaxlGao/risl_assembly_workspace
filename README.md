# RISL Assembly Workspace
This is a full ROS2 workspace for robotic assembly tasks using the UR5e robotic arm.

Environment: Ubuntu 22.04, ROS 2 Humble.

Component repositories are imported into src/ using vcstool. Commit component code changes in their respective repositories.

risl.repos tracks development branches; risl.lock.repos records a source snapshot.

Current repositories represented:
- https://github.com/MaxlGao/RISL_vention_ros
- https://github.com/MaxlGao/RISL_onrobot_ros
- https://github.com/MaxlGao/RISL_camera_msgs
- https://github.com/MaxlGao/RISL_ur
- https://github.com/MaxlGao/RISL_camera_localizer
- https://github.com/MaxlGao/RISL_simulation

To checkout:
```
git clone https://github.com/MaxlGao/risl_assembly_workspace.git ~/risl_assembly_ws
cd ~/risl_assembly_ws

mkdir -p src
vcs import src < risl.lock.repos
```

Required:
`pip install numpy cvxpy matplotlib pandas scipy scikit-learn opencv-python shapely trimesh pyswarms mujoco empy==3.3.4 catkin_pkg lark`