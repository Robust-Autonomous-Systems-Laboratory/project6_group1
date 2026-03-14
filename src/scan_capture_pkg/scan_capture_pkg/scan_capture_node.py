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
from datetime import datetime
from sensor_msgs.msg import LaserScan, PointCloud2, PointField
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Odometry

from interfaces_pkg.srv import CaptureScan

import numpy as np
import os
import yaml
import math

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



    def scan_callback(self, msg: LaserScan):
        self.latest_scan = msg

    def pose_callback(self, msg: PoseStamped):
        self.latest_pose = msg

    def odom_callback(self, msg: Odometry):
        if self.latest_pose is None:
            pose_msg = PoseStamped()
            pose_msg.header = msg.header
            pose_msg.pose = msg.pose.pose
            self.latest_pose = pose_msg

    def laserscan_to_pointcloud2(self, scan: LaserScan) -> PointCloud2:
       
        ranges = np.array(scan.ranges, dtype=np.float32)

        angles = scan.angle_min + np.arange(len(ranges), dtype=np.float32) * scan.angle_increment

        valid = (
            np.isfinite(ranges) &
            (ranges >= scan.range_min) &
            (ranges <= scan.range_max)
        )

        valid_ranges = ranges[valid]
        valid_angles = angles[valid]

        x = valid_ranges * np.cos(valid_angles)
        y = valid_ranges * np.sin(valid_angles)
        z = np.zeros_like(x, dtype=np.float32)

        points = np.stack((x, y, z), axis=1).astype(np.float32)
        data = points.tobytes()

        msg = PointCloud2()
        msg.header = scan.header
        msg.height = 1
        msg.width = points.shape[0]
        msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]
        msg.is_bigendian = False
        msg.point_step = 12  # 3 float32 values
        msg.row_step = msg.point_step * msg.width
        msg.is_dense = True
        msg.data = data

        return msg

    def quaternion_to_yaw(self, quaternion : Quaternion) -> float:
       w = quaternion.w
       x = quaternion.x
       y = quaternion.y
       z = quaternion.z
       yaw = math.atan2(2*(w*z + x*y), 1-2*(y**2 +  z**2))
       return yaw
    

    def save_capture(self, waypoint_id: int, description: str,
                     scan: LaserScan, pose: PoseStamped) -> str:
        """
        Save captured scan and pose to files.

        1. Generate a timestamped filename using waypoint_id
        2. Save pose data (x, y, yaw) and scan metadata to a YAML file
        3. Save raw range data to a .npy file alongside the YAML
        4. Return the path to the saved YAML file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f'waypoint_{waypoint_id:03d}_{timestamp}'

        yaml_path = os.path.join(self.output_dir, f'{base_name}.yaml')
        npy_path = os.path.join(self.output_dir, f'{base_name}.npy')

        px = float(pose.pose.position.x)
        py = float(pose.pose.position.y)
        yaw = float(self.quaternion_to_yaw(pose.pose.orientation))

        ranges = np.array(scan.ranges, dtype=np.float32)
        np.save(npy_path, ranges)

        metadata = {
            'waypoint_id': int(waypoint_id),
            'description': str(description),
            'timestamp': timestamp,
            'pose': {
                'frame_id': pose.header.frame_id,
                'x': px,
                'y': py,
                'yaw': yaw,
                'qx': float(pose.pose.orientation.x),
                'qy': float(pose.pose.orientation.y),
                'qz': float(pose.pose.orientation.z),
                'qw': float(pose.pose.orientation.w),
            },
            'scan': {
                'frame_id': scan.header.frame_id,
                'angle_min': float(scan.angle_min),
                'angle_max': float(scan.angle_max),
                'angle_increment': float(scan.angle_increment),
                'time_increment': float(scan.time_increment),
                'scan_time': float(scan.scan_time),
                'range_min': float(scan.range_min),
                'range_max': float(scan.range_max),
                'num_ranges': int(len(scan.ranges)),
                'ranges_file': os.path.basename(npy_path),
            }
        }

        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(metadata, f, sort_keys=False)

        return yaml_path
        

    def capture_callback(self, request, response):
        """
        Service callback: capture the current scan and pose.
        """
        if self.latest_scan is None:
            response.success = False
            response.message = 'No laser scan received yet.'
            response.filename = ''
            return response

        if self.latest_pose is None:
            response.success = False
            response.message = 'No pose estimate received yet.'
            response.filename = ''
            return response

        try:
            pointcloud_msg = self.laserscan_to_pointcloud2(self.latest_scan)
            self.pc_pub.publish(pointcloud_msg)

            saved_yaml = self.save_capture(
                request.waypoint_id,
                request.description,
                self.latest_scan,
                self.latest_pose
            )

            self.capture_count += 1

            response.success = True
            response.message = (
                f'Capture successful for waypoint {request.waypoint_id}. '
                f'Saved to {saved_yaml}'
            )
            response.filename = saved_yaml

            # Assuming the service response has a PoseStamped field named `pose`
            response.pose = self.latest_pose
            self.get_logger().info(response.message)

        except Exception as e:
            response.success = False
            response.message = f'Capture failed: {str(e)}'
            response.filename = ''
            self.get_logger().error(response.message)

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
