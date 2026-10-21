# RISL Assembly Workspace

Environment: Ubuntu 22.04, ROS 2 Humble.

Component repositories are imported into src/ using vcstool.
Commit component code changes in their respective repositories.

risl.repos tracks development branches.
risl.lock.repos records a source snapshot.

Validation status: clean build and hardware checks pending.

To checkout:
```
git clone https://github.com/MaxlGao/risl_assembly_workspace.git ~/risl_assembly_ws
cd ~/risl_assembly_ws

mkdir -p src
vcs import src < risl.lock.repos
```