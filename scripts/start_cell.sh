#!/usr/bin/env bash
set -e

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source /opt/ros/humble/setup.bash
source "$WORKSPACE_DIR/.venv/bin/activate"
source "$WORKSPACE_DIR/install/local_setup.bash"

exec ros2 launch risl_bringup cell.launch.py "$@"