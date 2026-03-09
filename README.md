# Project 6: Naive Mapping by Waypoints

## EE5531 Introduction to Robotics
---

## Introduction

In this project, you will build a map of an indoor environment by capturing laser scans at a series of waypoints while maintaining a continuous pose estimate. The primary objective is to evaluate the quality of the resulting map by comparing mapped geometry against physical measurements.

This project integrates or builds upon your previous work:
- **Dead reckoning** from odometry (Project 3)
- **Kalman filtering** for state estimation (Project 4)
- **Sensor characterization** and the beam model (Project 5)

You will develop a navigation strategy, collect scan data at waypoints, assemble the scans into a map, and quantitatively assess map accuracy.

---

## Learning Objectives

1. Build a point cloud map from multiple scan captures
2. Evaluate map accuracy by comparing mapped distances to physical measurements
3. Assess how localization drift affects map consistency
4. Apply your EKF/UKF implementation to real robot navigation
5. Work with ROS2 services and visualization tools

---

## The Mapping Problem

A map is only useful if it accurately represents the environment. This project evaluates map quality through two metrics:

**1. Distance Accuracy**

At each waypoint, you will:
- Measure the physical distance to a landmark (wall, corner, pillar) using a tape measure
- After building the map, measure the same distance in RViz using the Measure tool
- Compare: Does the map show the correct distance?

**2. Orientation Consistency**

At each waypoint, you will:
- Note which direction you're facing (e.g., "toward the north wall")
- After building the map, verify the landmark appears in the correct direction
- Check: Are features in the expected locations relative to each waypoint?

Poor localization causes scans to be placed incorrectly, resulting in:
- Distorted distances in the map
- Misaligned features (walls don't line up)
- "Ghosting" where the same wall appears twice

---

## Equipment

- TurtleBot3 Burger with LDS-01/LDS-02 LiDAR
- Masking tape for marking waypoints
- Tape measure for ground truth measurements
- Workstation with ROS2 Jazzy

---

## Project Instructions

### Part 1: Navigation Strategy (Written Plan)

Before data collection, develop a **written navigation strategy** including:

1. **Environment Selection**
   - Choose an area with clear landmarks (walls, corners, pillars)
   - Sketch the environment with landmark locations marked

2. **Waypoint Layout**
   - Plan at least 5 waypoints with good landmark visibility
   - Consider a loop closure (return near start) to check consistency

3. **Measurement Plan**
   - Which landmark will you measure at each waypoint?
   - How will you ensure consistent measurement points?

4. **Orientation Strategy**
   - How will you track robot heading at each waypoint?
   - Consider aligning with walls or floor tape for reference

Submit as `docs/navigation_strategy.md`.

### Part 2: Ground Truth Measurements

Before your data collection run:

1. **Mark waypoints** on the floor with masking tape

2. **Measure waypoint positions** (x, y) from the start position
   - You may do this one at a time, from one waypoint to the other

3. **At each waypoint, measure distance to a landmark**:
   - Choose a landmark visible in the LiDAR scan (wall, corner, pillar)
   - Measure from where the LiDAR center will be to the landmark
   - Record the landmark description and direction

4. **Record all measurements** in `config/measurements.yaml`

### Part 3: Data Collection

1. **Launch TurtleBot3 bringup** (provides /scan, /odom, /imu)

2. **Launch your localization node** (publishes /localization/pose)
   - Must publish `geometry_msgs/PoseStamped` to `/localization/pose`
   - You may use `ekf_node` or `ukf_node` from the `robot_localization` package (ROS2)

3. **Launch the scan capture service**:
   ```bash
   ros2 launch scan_capture_pkg scan_capture.launch.py
   ```

4. **Start bag recording**:
   ```bash
   ros2 bag record -o mapping_run /scan /odom /imu /localization/pose /scan_capture/pointcloud
   ```

5. **Open RViz** with the provided config:
   ```bash
   rviz2 -d scan_capture_pkg/config/mapping.rviz
   ```

6. **Navigate to each waypoint**:
   ```bash
   ros2 run turtlebot3_teleop teleop_keyboard
   ```

7. **At each waypoint**:
   - Stop completely and wait 1-2 seconds
   - Verify you're at the tape mark and facing the planned direction
   - Capture the scan:
     ```bash
     ros2 run scan_capture_pkg keyboard_capture.py
     # Press 1-9 for waypoint ID, or 's' for auto-increment
     ```
   - Take an RViz screenshot showing the current scan and pose

### Part 4: Map Assembly and Evaluation

After data collection:

1. **Visualize all captured point clouds** in RViz
   - Load each saved point cloud (from `data/captures/`)
   - All clouds share the `odom` frame, so they should align

2. **Evaluate distance accuracy** at each waypoint:
   - Use RViz's **Measure tool** (or Publish Point + manual calculation)
   - Measure the distance from each waypoint position to its landmark
   - Compare against your tape-measure ground truth
   - Record results in `config/measurements.yaml`

3. **Evaluate orientation consistency**:
   - At each waypoint, is the landmark in the expected direction?
   - Do walls from different scans align, or are they offset?
   - Take screenshots showing alignment quality

4. **Check for mapping artifacts**:
   - Double walls (same wall captured from two positions doesn't align)
   - Gaps or overlaps in features
   - Drift accumulation visible in loop closure

### Part 5: Analysis and Documentation

Complete your README with:

**Distance Accuracy Table**

| Waypoint | Landmark | Measured (m) | RViz (m) | Error (m) | Error (%) |
|----------|----------|--------------|----------|-----------|-----------|
| 1 | North wall | 2.35 | 2.31 | 0.04 | 1.7% |
| 2 | East corner | 1.82 | 1.89 | 0.07 | 3.8% |
| ... | ... | ... | ... | ... | ... |

**Orientation Assessment**

For each waypoint, describe:
- Expected landmark direction vs. observed direction in map
- Any rotational misalignment between scans

**Map Quality Discussion**

- Overall distance accuracy (mean/max error)
- Sources of error (localization drift, measurement uncertainty)
- Map consistency (do features align across scans?)
- How would your Project 4 sensor calibration improve results?

---

## Using RViz Measure Tool

To measure distances in RViz:

1. Click the **Measure** tool in the toolbar (ruler icon)
2. Click on the first point (waypoint location)
3. Click on the second point (landmark)
4. The distance appears in the tool output

Alternative: Use **Publish Point** tool and compute distance from coordinates.

---

## Team Structure

Teams of two. Both members contribute to strategy, data collection, and documentation. All students must make
substantial contributions to your repository to receive credit. 

---

## Deliverables

Submit via your team's **class GitHub repository**.

### Repository Structure

```
proj5-waypoint-mapping/
├── README.md                    # Project report
├── docs/
│   └── navigation_strategy.md  # Written strategy
├── scan_capture_pkg/           # ROS2 package
│   └── config/
│       └── measurements.yaml   # Ground truth + results
├── data/
│   ├── captures/               # Captured point clouds and poses
│   └── mapping_run/            # Bag file (or link)
└── figures/
    ├── rviz_screenshots/       # Screenshots at each waypoint
    └── map_evaluation/         # Screenshots showing measurements
```

### README Requirements

#### 1. Navigation Strategy Summary (5 pts)
- Environment sketch with waypoints and landmarks
- Reference to full strategy in `docs/`

#### 2. System Architecture (5 pts)
- Data flow diagram
- Your EKF/UKF configuration summary
- How you would incorporate Project 4 sensor calibration

#### 3. Map Accuracy Results (15 pts)
- Distance accuracy table (all waypoints)
- Orientation assessment for each waypoint
- RViz screenshots showing:
  - Individual scan captures at each waypoint
  - Measurement tool usage
  - Overall map with all scans visualized

#### 4. Discussion (10 pts)
- Analysis of mapping accuracy
- Sources of error (localization, measurement, sensor)
- Map consistency assessment
- Recommendations for improvement

#### 5. Usage Instructions (5 pts)
- How to launch your localization node
- How to run the scan capture system
- How to visualize the captured map

### Code and Data (10 pts)
- Completed `measurements.yaml` with ground truth and results
- Bag file from your mapping run
- Git history with contributions from both team members

---

## Grading Rubric

| Component | Points |
|-----------|--------|
| Navigation strategy summary | 5 |
| System architecture documentation | 5 |
| Map accuracy results (table, orientation, screenshots) | 15 |
| Discussion and analysis | 10 |
| Usage instructions | 5 |
| Code quality and data submission | 10 |
| **Total** | **50** |

---

## Hints and Tips

### Choosing Good Landmarks

- **Walls**: Measure perpendicular distance to wall surface
- **Corners**: Measure to the corner point (clear in LiDAR)
- **Pillars**: Measure to center or nearest surface
- Avoid: Moving objects, glass, highly reflective surfaces

### Ensuring Measurement Consistency

- Mark the exact measurement point on landmarks with tape if possible
- Always measure from the LiDAR center position (not robot front)
- Use the same measurement technique in RViz (point to same feature)

### Orientation Reference

Since heading is hard to measure precisely:
- Align robot parallel to a wall at each waypoint (heading is then known relative to wall)
- Place tape lines on floor to define heading directions
- Use compass directions if walls are aligned with cardinal directions
- Document your reference system in the strategy

### Detecting Localization Drift

If you return near the start position (loop closure):
- The start landmark should be at nearly the same distance
- If distances differ significantly, you've accumulated drift
- This is valuable data for your discussion section

---

## References

1. Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press. (Chapter 9: Occupancy Grid Mapping)
2. TurtleBot3 Manual: https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/
