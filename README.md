# Route Optimization & Constraint-Based Scheduling Engine

## Project Overview

This project is a Python-based implementation of a route planning and scheduling system.

It generates an optimized visit order for multiple locations starting and ending at **HQ** while considering:

* Travel time
* Service time
* Time window constraints

The solution is built using **greedy heuristic methods** and does not use any external optimization libraries.


## Algorithms Used

This project uses a **Greedy Heuristic Optimization** approach with three classic strategies:

### 1. Nearest Neighbor

* Selects the closest unvisited location from the current position
* Helps reduce travel distance

### 2. Earliest Deadline First (EDF)

* Prioritizes locations based on earliest closing time
* Helps avoid missing tight time windows

### 3. Shortest Service Time First

* Locations with smaller service durations are visited earlier
* Helps complete more visits in limited time


## Final Route Selection Logic

Each strategy generates one possible route.

All routes are simulated, and the best one is selected based on:

1. Maximum number of locations successfully visited
2. Minimum total travel time (if visit counts are equal)

This makes the system simple, efficient, and constraint-aware.


## Implementation Details

The system works in the following steps:

1. Read input data from a JSON file

2. Extract:

   * Locations (including HQ)
   * Distance matrix
   * Service time per location
   * Time windows

3. Generate candidate routes using:

   * Nearest Neighbor
   * Earliest Deadline First
   * Shortest Service Time

4. Simulate time flow for each route:

   * Calculate travel time
   * Check arrival time
   * Wait if early
   * Skip if arrival is after latest allowed time
   * Add service time

5. Add return travel time back to HQ

6. Compare all routes and select the best one

7. Save the result into an output file


## Input Format

The program expects a JSON file with the following fields:

* `locations` → List of all locations (must include "HQ")
* `distance` → Distance/time matrix between locations
* `service_time` → Service duration at each location
* `time_window` → `[earliest, latest]` allowed time for each location

### Example Input

```json
{
  "locations": ["HQ", "A", "B", "C"],
  "distance": {
    "HQ": {"HQ": 0, "A": 10, "B": 15, "C": 20},
    "A": {"HQ": 10, "A": 0, "B": 5, "C": 8},
    "B": {"HQ": 15, "A": 5, "B": 0, "C": 6},
    "C": {"HQ": 20, "A": 8, "B": 6, "C": 0}
  },
  "service_time": {
    "HQ": 0,
    "A": 10,
    "B": 15,
    "C": 5
  },
  "time_window": {
    "HQ": [0, 1000],
    "A": [0, 50],
    "B": [20, 80],
    "C": [10, 40]
  }
}
```

## Requirements

* Python 3.7 or above
* No external libraries required

Built-in modules used:

* argparse
* json
* os
* sys
  
## Project Structure

```
project/
│
├── main.py
├── inputs/
│   └── input1.json
├── outputs/
└── README.md
```


## How to Run

### Run with Input File

```bash
python main.py --input inputs/input1.json
```

### Run with Custom Output File

```bash
python main.py --input inputs/input1.json --output outputs/result.txt
```

## Output Details

The output file contains:

* Best strategy used
* Final route (HQ → locations → HQ)
* Total travel time (including return to HQ)
* Total service time
* Total waiting time (idle time)
* Total duration
* Detailed visit timing
* Skipped locations with reason


## Assumptions

* Route always starts and ends at HQ
* If arrival is early, the vehicle waits
* If arrival is late, the location is skipped
* Travel time is taken from the distance matrix
* Missing distances are treated as large values
