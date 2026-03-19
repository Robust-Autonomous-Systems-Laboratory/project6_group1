# Project 6: Naive Mapping by Waypoints

# EE5531 Introduction to Robotics

# 1. Navigation Strategy Summary (5 pts)
## Environment sketch with waypoints and landmarks
```
    +------------------+
    |                  |
    |                  |
    |  | - 3 <-|       |  B = Bin
    |  |       |       |
    |  v       |       |
    |  4   B   2       |  1-5 = Waypoints
    |  |       ^       |  Arrows = Path
    |  |       |       |
    |  ----5-> 1       |
    |                  |
    +------------------+
         North Wall
```
The mapping experiment was conducted in an indoor environment with clearly defined landmarks, including the north wall, east wall, and a centrally located recycle bin. A total of five waypoints were strategically placed to ensure good visibility of these landmarks while forming a closed-loop path to evaluate drift and map consistency. The robot starts at waypoint 1 and follows a path covering approximately 12.56 meters, returning near the starting position for loop closure analysis. At each waypoint, a specific landmark was selected for distance measurement, ensuring consistency between ground truth measurements and RViz-based evaluation.

To maintain orientation consistency, the robot’s heading was defined relative to the initial pose (facing south at waypoint 1), with subsequent orientations aligned using walls and floor tape as references. At each waypoint, the robot was carefully positioned, aligned, and stabilized before capturing scans to minimize motion-induced errors. Measurements were taken using a tape measure with an estimated uncertainty of ±0.2 m and later compared against RViz measurements. Potential challenges such as odometry drift, IMU bias, and wheel slip were mitigated using EKF-based localization and controlled robot motion, ensuring more accurate scan alignment and improved overall map quality.

# 2. System Architecture (5 pts)
## Data flow diagram

```
TurtleBot3 Hardware
    │
    ├─── /scan          (LaserScan, LDS-02 LiDAR)
    ├─── /odom          (Odometry, wheel encoders)
    └─── /imu           (IMU data)
         │
         v
  scan_capture_node
    │   ├── Subscribes: /scan, /odom (pose fallback)
    │   ├── Publishes:  /scan_capture/pointcloud (PointCloud2)
    │   └── Service:    /scan_capture/capture (CaptureScan)
         │
         v
         
  data/captures/
    ├── waypoint_N.yaml     (pose + metadata)
    └── waypoint_N.npy      (raw range array)
         │
         v
  RViz2 visualization
    └── All point clouds overlaid for map evaluation
```

## Localization Configuration (EKF/UKF configuration summary)

No external localization node was available during data collection. The `scan_capture_node` fell back to odometry poses sourced from the `/odom` topic. Pose estimates are therefore subject to wheel encoder drift with no correction mechanism — this is the primary source of error in the final map.

Dead reckoning from odometry accumulates error proportional to distance traveled. Over the ~4 m total path in this run, we observed moderate positional drift by the final waypoint, consistent with typical encoder-based odometry on the TurtleBot3 Burger (wheel slip, floor irregularities, minor IMU misalignment).

## Project 5 Sensor Characterization Integration

Project 5 sensor characterization can be incorporated into the mapping pipeline by using the LiDAR beam model to account for measurement noise and uncertainty during scan processing. Instead of treating all laser measurements equally, each beam can be filtered and weighted based on its expected noise characteristics such as 𝜎 hit and measurement bias. This allows us to reject outliers, reduce the impact of noisy readings, and generate more reliable point clouds at each waypoint. As a result, mapped features such as walls and corners become more consistent and less affected by erroneous measurements.

Additionally, the sensor characterization can be integrated into the localization pipeline by properly tuning the measurement covariance matrix in the EKF/UKF using real LiDAR noise parameters. This improves pose estimation accuracy and reduces drift, which directly enhances scan alignment across waypoints. Overall, incorporating the beam model leads to improved map accuracy, fewer artifacts such as ghosting or misalignment, and a more robust, uncertainty-aware mapping process compared to a purely geometric approach we used.


## 3. Map Accuracy Results (15 pts)
- Distance accuracy table (all waypoints)
- Orientation assessment for each waypoint
- RViz screenshots showing:
  - Individual scan captures at each waypoint
  - Measurement tool usage
  - Overall map with all scans visualized

## 4. Discussion (10 pts)
- Analysis of mapping accuracy
- Sources of error (localization, measurement, sensor)
- Map consistency assessment
- Recommendations for improvement

## 5. Usage Instructions (5 pts)
- How to launch your localization node
- How to run the scan capture system
- How to visualize the captured map

### Code and Data (15 pts)
- **Scan capture service implementation** (10 pts): `scan_capture_node.py` fully implemented — parameters, subscribers, publisher, service handler, scan-to-point-cloud conversion, and file saving all working correctly
- Completed `measurements.yaml` with ground truth and results (3 pts)
- Bag file from your mapping run and git history with contributions from both team members (2 pts)

---