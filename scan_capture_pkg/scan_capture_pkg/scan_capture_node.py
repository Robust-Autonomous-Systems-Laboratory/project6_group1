#!/usr/bin/env python3
"""
Scan Capture Service Node

This node provides a service to capture laser scans at waypoints.
It subscribes to /scan and /localization/pose, and when triggered,
saves the current scan as a PointCloud2 along with the pose estimate.

Author: [Student Team]
Course: EE5531 Introduction to Robotics
Project: 6 - Waypoint Mapping
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import LaserScan, PointCloud2, PointField
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

from scan_capture_pkg.srv import CaptureScan

import numpy as np
import os
import yaml


class ScanCaptureNode(Node):
    """
    ROS2 node providing scan capture service for waypoint mapping.

    TODO: Implement this node to:
    - Subscribe to /scan (LaserScan) and /localization/pose (PoseStamped)
    - Provide a /scan_capture/capture service (CaptureScan)
    - When the service is called, convert the latest scan to PointCloud2,
      publish it, and save the scan data and pose to files in output_dir
    """

    def __init__(self):
        super().__init__('scan_capture_node')

        # =====================================================================
        # Parameters
        # =====================================================================
        self.declare_parameter('output_dir', 'data/captures')
        self.declare_parameter('pose_topic', '/localization/pose')
        self.declare_parameter('scan_topic', '/scan')

        self.output_dir = self.get_parameter('output_dir').get_parameter_value().string_value
        self.pose_topic = self.get_parameter('pose_topic').get_parameter_value().string_value
        self.scan_topic = self.get_parameter('scan_topic').get_parameter_value().string_value

        os.makedirs(self.output_dir, exist_ok=True)

        # =====================================================================
        # State variables
        # =====================================================================
        self.latest_scan = None
        self.latest_pose = None
        self.capture_count = 0

        # =====================================================================
        # QoS
        # =====================================================================
        scan_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        default_qos = 10

        # =====================================================================
        # Subscribers
        # =====================================================================
        self.scan_sub = self.create_subscription(
            LaserScan,
            self.scan_topic,
            self.scan_callback,
            scan_qos
        )

        self.pose_sub = self.create_subscription(
            PoseStamped,
            self.pose_topic,
            self.pose_callback,
            default_qos
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            default_qos
        )

        # =====================================================================
        # Publishers
        # =====================================================================
        self.pc_pub = self.create_publisher(
            PointCloud2,
            '/scan_capture/pointcloud',
            10
        )

        # =====================================================================
        # Service
        # =====================================================================
        self.capture_srv = self.create_service(
            CaptureScan,
            '/scan_capture/capture',
            self.capture_callback
        )

        self.get_logger().info('Scan Capture Node started')
        self.get_logger().info(f'  scan_topic: {self.scan_topic}')
        self.get_logger().info(f'  pose_topic: {self.pose_topic}')
        self.get_logger().info(f'  output_dir: {self.output_dir}')



        self.get_logger().info('Scan Capture Node started (stub - not yet implemented)')

    def scan_callback(self, msg: LaserScan):
        """Store the latest laser scan."""
        # TODO: Save the incoming scan message to a member variable
        pass

    def pose_callback(self, msg: PoseStamped):
        """Store the latest pose estimate."""
        # TODO: Save the incoming pose message to a member variable
        pass

    def odom_callback(self, msg: Odometry):
        """Fallback: use odometry pose if no localization pose is available."""
        # TODO: If no pose has been received yet, convert the Odometry message
        #       to a PoseStamped and store it
        pass

    def laserscan_to_pointcloud2(self, scan: LaserScan) -> PointCloud2:
        """
        Convert a LaserScan message to PointCloud2.

        TODO: Implement the conversion:
        1. Compute Cartesian (x, y) coordinates from range and angle data
        2. Filter out invalid ranges (outside [range_min, range_max] or non-finite)
        3. Build and return a PointCloud2 message with XYZ float32 fields
           in the same frame as the input scan
        """
        raise NotImplementedError('laserscan_to_pointcloud2 not yet implemented')

    def save_capture(self, waypoint_id: int, description: str,
                     scan: LaserScan, pose: PoseStamped) -> str:
        """
        Save captured scan and pose to files.

        TODO: Implement file saving:
        1. Generate a timestamped filename using waypoint_id
        2. Save pose data (x, y, yaw) and scan metadata to a YAML file
        3. Save raw range data to a .npy file alongside the YAML
        4. Return the path to the saved YAML file
        """
        raise NotImplementedError('save_capture not yet implemented')

    def capture_callback(self, request, response):
        """
        Service callback: capture the current scan and pose.

        TODO: Implement the service handler:
        1. Check that latest scan and pose data are available; return a
           failure response with an informative message if either is missing
        2. Convert the scan to PointCloud2 and publish it
        3. Save the scan and pose using save_capture()
        4. Populate and return the response (success, message, filename, pose)
        """
        response.success = False
        response.message = 'Not yet implemented'
        response.filename = ''
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ScanCaptureNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
