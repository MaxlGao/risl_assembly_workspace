from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    ur_launch = (
        Path(get_package_share_directory('ur_robot_driver'))
        / 'launch'
        / 'ur_control.launch.py'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_ip', default_value='192.168.1.111'
        ),
        DeclareLaunchArgument(
            'start_driver', default_value='true'
        ),
        DeclareLaunchArgument(
            'start_localization', default_value='true'
        ),
        DeclareLaunchArgument(
            'start_simulation', default_value='true'
        ),
        DeclareLaunchArgument(
            'start_allocation', default_value='false'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(ur_launch)),
            condition=IfCondition(LaunchConfiguration('start_driver')),
            launch_arguments={
                'ur_type': 'ur5e',
                'robot_ip': LaunchConfiguration('robot_ip'),
                'use_mock_hardware': 'false',
                'use_tool_communication': 'true',
                'tool_baud_rate': '1000000',
                'tool_voltage': '24',
                'tool_parity': '2',
                'tool_stop_bits': '1',
                'tool_rx_idle_chars': '1.5',
                'tool_tx_idle_chars': '3.5',
                'launch_rviz': 'false',
            }.items(),
        ),

        Node(
            package='risl_onrobot_ros',
            executable='gripper_control',
            output='screen',
        ),

        Node(
            package='risl_camera_localizer',
            executable='localize',
            condition=IfCondition(
                LaunchConfiguration('start_localization')
            ),
            output='screen',
        ),
        Node(
            package='risl_camera_localizer',
            executable='allocate',
            condition=IfCondition(
                LaunchConfiguration('start_allocation')
            ),
            output='screen',
        ),
        Node(
            package='risl_simulation',
            executable='simulation_node',
            condition=IfCondition(
                LaunchConfiguration('start_simulation')
            ),
            output='screen',
        ),
    ])