# Navigation and Measurement Strategy

## Team Members
- Member 1: Progress Munoriarwa
- Member 2: Reid Beckes

---

## 1. Environment Description

### Location
A rectangular indoor room approximately 5 m × 4 m. The floor is hard linoleum tile. The room has four well-defined flat walls with no large windows on the mapped sides. Some interior obstacles (chairs, small equipment) are present but were avoided during navigation. The south wall and east wall were the clearest, most unobstructed surfaces and served as the primary measurement landmarks.

### Environment Sketch
```
        West Wall
    +------------------+
    |        4         |
    |   5         3    |
    |                  |
    |      [obst]      |
    |                  |
    |   1         2    |
    |                  |
    +------------------+
        South Wall       East Wall -->

    1–5 = Waypoints
    [obst] = Interior obstacles (chairs/equipment)
    Robot started at WP1, facing north
    Path: 1 → 2 → 3 → 4 → 5
```

### Identified Landmarks
| ID | Landmark | Location | Notes |
|----|----------|----------|-------|
| A  | South wall | South side of room | Flat, unobstructed — primary reference at WP1/WP2 |
| B  | East wall | East side of room | Flat, good visibility from WP2 and WP3 |
| C  | North wall | North side of room | Visible from WP4; some fragmentation due to drift |
| D  | West wall | West side of room | Visible from WP5; furthest from start |

---

## 2. Waypoint Plan

### Waypoint Layout

| Waypoint | Position (x, y) | Landmark to Measure | Measurement Direction |
|----------|-----------------|---------------------|----------------------|
| 1 (Start)| (0.0, 0.0) | South wall | Behind robot (180°) |
| 2 | (1.5, 0.0) | East wall | Right of robot (270°) |
| 3 | (1.5, 1.5) | East wall | Right of robot (270°) |
| 4 | (0.5, 2.5) | North wall | Ahead of robot (0°) |
| 5 | (0.0, 1.5) | West wall | Left of robot (90°) |

### Path Statistics
- Number of waypoints: 5
- Total path length: ~6.5 m
- Loop closure planned: No (path ends near start but no explicit return)
- Estimated navigation time: ~10–15 minutes including scan captures

---

## 3. Orientation Strategy

### Heading Reference System
At each waypoint, the robot was aligned parallel to the nearest wall using the room's grid geometry as a reference. Floor tape marks at each waypoint included a short directional arrow (~20 cm) indicating the intended forward heading. This ensured the robot's x-axis was consistently orthogonal or parallel to the wall being measured.

- [x] Align robot parallel to a specific wall at each waypoint
- [x] Use floor tape lines to define heading

### At Each Waypoint
| Waypoint | Orientation Reference | Expected Landmark Direction |
|----------|----------------------|----------------------------|
| 1 | Parallel to south wall, facing north | South wall directly behind (180°) |
| 2 | Parallel to south wall, facing north | East wall to the right (270°) |
| 3 | Parallel to east wall, facing north | East wall to the right (270°) |
| 4 | Parallel to north wall, facing north | North wall directly ahead (0°) |
| 5 | Parallel to west wall, facing east | West wall to the left (90°) |

---

## 4. Measurement Protocol

### Before Data Collection
- [x] Mark all waypoints with tape
- [x] Measure waypoint positions from start
- [x] Identify measurement landmark at each waypoint
- [x] Measure distance to each landmark
- [x] Record all measurements in `config/measurements.yaml`

### At Each Waypoint During Collection
1. [x] Stop robot completely at tape mark
2. [x] Align robot to planned orientation
3. [x] Wait 2 seconds for settling
4. [x] Verify landmark visible in RViz scan
5. [x] Capture scan with waypoint ID
6. [x] Take RViz screenshot
7. [x] Note any observations

### Measurement Technique
- Measuring from: LiDAR center (approximately 10 cm forward of robot geometric center)
- Measuring to: Wall surface (perpendicular distance)
- Tool: Tape measure
- Estimated measurement uncertainty: ± 0.02 m

---

## 5. Expected Challenges

### Localization Error Sources
1. **Odometry drift**: Expected to accumulate over the ~6.5 m path. No EKF or UKF was used, so all pose estimates came from wheel encoder integration. Mitigation: minimize unnecessary turns, move slowly and steadily between waypoints.
2. **IMU bias**: IMU data was available on `/imu` but not fused into the pose estimate for this run. Expected impact is primarily on heading accuracy during turns. Mitigation: align to wall markings at each waypoint rather than relying on odometry heading alone.
3. **Wheel slip**: The linoleum floor has low but nonzero slip risk, particularly during in-place rotations. Mitigation: use slow rotation speed during heading corrections.

### Mapping Challenges
1. **Scan alignment**: Without a global localization reference, scans from later waypoints will be placed using drifted odometry poses, causing walls to appear shifted or doubled in the overlay.
2. **Landmark visibility**: Interior obstacles (chairs, small equipment) are partially visible in the LiDAR scan and could obscure wall surfaces at some angles. Waypoints were positioned to minimize this.
3. **Environmental factors**: The room is an active lab space. We collected data during a low-traffic period to reduce moving-person detections in the scan.

### Mitigation Strategies
- Slow, deliberate navigation between waypoints to minimize wheel slip
- 2-second pause before each capture to allow scan to stabilize
- Tape arrows at each waypoint for consistent heading alignment
- Chose wall landmarks (rather than furniture) for reliable, repeatable measurements

---

## 6. Roles During Data Collection

| Task | Team Member |
|------|-------------|
| Robot pilot (teleop keyboard) | Reid Beckes |
| RViz monitoring / screenshots | Progress Munoriarwa |
| Scan capture triggering | Progress Munoriarwa |
| Observation notes | Reid Beckes |

---

## 7. Post-Collection Analysis Plan

### Map Evaluation Steps
1. [x] Load all point clouds in RViz via bag replay
2. [x] Verify scans appear in `odom` frame
3. [x] For each waypoint, measure distance to landmark using RViz Measure tool
4. [x] Record RViz measurements in `measurements.yaml`
5. [x] Compute errors (tape measure − RViz)
6. [x] Take screenshots showing measurements
7. [x] Assess orientation consistency at each waypoint

### Quality Checks
- [x] Do walls from different scans align? — Partial. South/east walls align well; north/west walls show drift artifacts.
- [ ] Is loop closure consistent? — No explicit loop closure was performed.
- [x] Are there any obvious mapping artifacts? — Yes: south wall double-line at WP5, fragmented north wall at WP4.

---

## 8. Pre-Run Checklist

- [x] Robot battery charged
- [x] All waypoints marked with tape
- [x] All positions measured and recorded
- [x] All landmark distances measured and recorded
- [x] `measurements.yaml` filled with ground truth
- [ ] Localization node tested — odometry fallback used instead
- [x] Scan capture service tested
- [x] RViz configured
- [x] Bag recording tested
- [x] Camera/screenshot tool ready
- [x] This strategy document complete