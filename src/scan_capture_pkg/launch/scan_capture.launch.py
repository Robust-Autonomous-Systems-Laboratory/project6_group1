#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    output_dir_arg = DeclareLaunchArgument(
        'output_dir',
        default_value='data/captures',
        description='Directory to save captured scans'
    )

    pose_topic_arg = DeclareLaunchArgument(
        'pose_topic',
        default_value='/localization/pose',
        description='Topic to subscribe for pose estimates'
    )

    scan_topic_arg = DeclareLaunchArgument(
        'scan_topic',
        default_value='/scan',
        description='Topic to subscribe for laser scans'
    )

    # Get launch configurations
    output_dir = LaunchConfiguration('output_dir')
    pose_topic = LaunchConfiguration('pose_topic')
    scan_topic = LaunchConfiguration('scan_topic')

    # Scan capture service node
    scan_capture_node = Node(
        package='scan_capture_pkg',
        executable='scan_capture_node',
        name='scan_capture_node',
        output='screen',
        parameters=[{
            'output_dir': output_dir,
            'pose_topic': pose_topic,
            'scan_topic': scan_topic
        }]
    )

    return LaunchDescription([
        output_dir_arg,
        pose_topic_arg,
        scan_topic_arg,
        scan_capture_node,
    ])