# Navigation and Measurement Strategy

## Team Members
- Member 1: Progress Munoriarwa
- Member 2: Reid Beckes

---

## 1. Environment Description

### Location
[Describe the room/area: dimensions, floor type, notable features]

### Environment Sketch
```
[Draw ASCII sketch of environment with walls, landmarks, and planned waypoints]

Example:
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

### Identified Landmarks
| ID | Landmark | Location | Notes |
|----|----------|----------|-------|
| A  | North wall | North side | Flat surface, good for distance measurement |
| B  | Recycle Bin | Center |  Part of it is prominent in all scans |
| C  | East Wall | East side | Flat surface but not all of it may be visible at every wayppoint |

---

## 2. Waypoint Plan

### Waypoint Layout

| Waypoint | Position (x, y) (cm) | Landmark to Measure | Measurement Direction |
|----------|-----------------|---------------------|----------------------|
| 1 (Start)| (0, 0) | North wall, Recycle Bin | South (0°) |
| 2 | (179, 0) | Recycle Bin | South (0°) |
| 3 | (343, 174) | Recycle Bin | East (90°) |
| 4 | (174, 285) | Recycle Bin | North (180°) |
| 5 | (0, 131) | North wall, Recycle Bin | West (270°) |

### Path Statistics
- Number of waypoints: 5
- Total path length: 12.56m
- Loop closure planned: Yes
- Estimated navigation time: 30 min

---

## 3. Orientation Strategy

### Heading Reference System
Orientation is in reference to the 1st waypoint where the robot is facing south. The rotaitons are then done counterclockwise from that orientation (S-E-N-W). The orientations are aligned based on the walls and are marked out by tape.


### At Each Waypoint
| Waypoint | Orientation Reference | Expected Landmark Direction |
|----------|----------------------|----------------------------|
| 1 | Prependicualar to North Wall facing South | North wall at 180° and recycle bin at roughly 60°|
| 2 | Prependicualar to North Wall facing South | North wall at 180° and recycle bin at roughly 90°|
| 3 | Parallel to North Wall facing East | Recycle bin at 90° | 
| 4 | Perpendicular to North Wall facing North | Recycle bin at 90° and north wall at 0° |
| 5 | Parallel to North Wall facing West | North wall at 270° and recycle bin at roughly 30°|

---

## 4. Measurement Protocol

### Before Data Collection
- [ ] Mark all waypoints with tape
- [ ] Measure waypoint positions from start
- [ ] Identify measurement landmark at each waypoint
- [ ] Measure distance to each landmark
- [ ] Record all measurements in `config/measurements.yaml`

### At Each Waypoint During Collection
1. [ ] Stop robot completely at tape mark
2. [ ] Align robot to planned orientation
3. [ ] Wait 2 seconds for settling
4. [ ] Verify landmark visible in RViz scan
5. [ ] Capture scan with waypoint ID
6. [ ] Take RViz screenshot
7. [ ] Note any observations

### Measurement Technique
- Measuring from: tape mark
- Measuring to: nearest landmark point
- Tool: tape measure
- Estimated measurement uncertainty: ± 0.2 m

---

## 5. Expected Challenges

### Localization Error Sources
1. **Odometry drift**: Can cause errors with the localization system leading to misalinment between later wayporints.
2. **IMU bias**: Similar to odometry drift, will compound and further cause more localization issue which will lead to misalignment as the robot travels.
3. **Wheel slip**: Can cause error both with odometry and localization and also the physical travel of the robot.

### Mapping Challenges
1. **Scan alignment**: Scans will likely misalingn due to the issue mentioned above. If enough drift occurs, waypoints might misalign.
2. **Landmark visibility**: Because the recycle bin is the center of the waypoints, there should be no issues capturing the landmark.
3. **Environmental factors**: People moving around can objects in different places for the various scans.

### Mitigation Strategies
- Wheel Slip - clean floors
- Wheel Slip - avoid quick turns
- Odemetry drift/IMU bias - use EKF to help mitigate drift

---

## 6. Roles During Data Collection

| Task | Team Member |
|------|-------------|
| Robot pilot | Reid |
| RViz monitoring / screenshots | Progress Munoriarwa |
| Scan capture triggering | Progress Munoriarwa |
| Observation notes | Reid |

---

## 7. Post-Collection Analysis Plan

### Map Evaluation Steps
1. [x] Load all point clouds in RViz
2. [x] Verify scans appear in `odom` frame
3. [x] For each waypoint, measure distance to landmark using RViz Measure tool
4. [x] Record RViz measurements in `measurements.yaml`
5. [x] Compute errors (measured - RViz)
6. [x] Take screenshots showing measurements
7. [x] Assess orientation consistency at each waypoint

### Quality Checks
- [x] Do walls from different scans align?
- [x] Is loop closure consistent (if applicable)?
- [x] Are there any obvious mapping artifacts?

---

## 8. Pre-Run Checklist

- [X] Robot battery charged
- [x] All waypoints marked with tape
- [x] All positions measured and recorded
- [x] All landmark distances measured and recorded
- [x] `measurements.yaml` filled with ground truth
- [x] Localization node tested
- [x] Scan capture service tested
- [x] RViz configured
- [x] Bag recording tested
- [x] Camera/screenshot tool ready
- [x] This strategy document complete
