# Route Optimization & Constraint-Based Scheduling Engine

## Project Overview

This project is a Python-based implementation of a route planning and scheduling system.
It generates an optimized visit order for multiple locations starting and ending at HQ while considering travel time, service time, and time window constraints.

The solution is built using greedy heuristic methods and does not use any external optimization libraries.


## Algorithms Used

This project uses a **Greedy Heuristic Optimization approach** with three classic strategies:

### 1. Nearest Neighbor Algorithm

* Selects the closest unvisited location from the current position
* Helps reduce travel distance

### 2. Earliest Deadline First (EDF) Scheduling

* Locations are prioritized based on the earliest closing time of their time window
* Helps avoid missing tight time constraints

### 3. Shortest Service Time First

* Locations with smaller service durations are visited earlier
* Helps complete more visits in limited time

### Final Route Selection Logic

Each strategy generates one possible route.
All routes are simulated, and the best one is selected based on:

1. Maximum number of locations successfully visited
2. Minimum total travel time

This makes the solution simple, fast, and suitable for constraint-based scheduling.


## Implementation Details

The system works in the following steps:

1. Read input data from a JSON file
2. Extract:

   * Locations (including HQ)
   * Distance matrix
   * Service time per location
   * Time windows
3. Generate 3 candidate routes using:

   * Nearest Neighbor
   * Earliest Deadline
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

* `locations` – List of all locations (must include "HQ")
* `distance` – Distance/time matrix between locations
* `service_time` – Service duration at each location
* `time_window` – [earliest, latest] allowed time for each location

### Example Structure

```
{
  "locations": ["HQ", "A", "B", "C"],
  "distance": {
    "HQ": {"A": 10, "B": 15, "C": 20},
    "A": {"HQ": 10, "B": 5, "C": 8},
    "B": {"HQ": 15, "A": 5, "C": 6},
    "C": {"HQ": 20, "A": 8, "B": 6}
  },
  "service_time": {
    "A": 10,
    "B": 15,
    "C": 5
  },
  "time_window": {
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


## Project Setup Instructions

### Step 1: Install Python

Check if Python is installed:

```
python --version
```

If not installed, install Python 3.x.

---

### Step 2: Project Folder Structure

Create the following structure:

```
project/
│
├── main.py
├── inputs/
│   └── input1.json
├── outputs/
└── README.md
```

---

### Step 3: Add Input File

Place your JSON file inside the `inputs` folder.

Example:

```
inputs/input1.json
```

---

## How to Run

### Run with Custom Input

```
python main.py --input inputs/input2.json
```

### Run with Custom Output File

```
python main.py --input inputs/input1.json --output outputs/result.txt
```



## Output Details

The output file contains:

* Best strategy used
* Final route (HQ → locations → HQ)
* Total travel time (including return to HQ)
* Total service time
* Total waiting time
* Total duration
* Detailed visit timing
* Skipped locations with reason



## Assumptions

* Route always starts and ends at HQ
* If arrival is early, vehicle waits
* If arrival is late, location is skipped
* Travel time is taken from the distance matrix
* Missing distances are treated as large values


