## Explanation of Algorithm, Logic, and Assumptions

### Algorithm / Logic Used

This project solves the route optimization problem using a **Greedy Heuristic-Based Scheduling Approach**. Since the problem involves time windows, travel time, and service duration constraints, an exact mathematical solution is complex. Therefore, multiple simple decision strategies are used and the best result is selected after simulation.

The system works in the following stages:

**1. Input Processing**

* The program reads a JSON input file containing:

  * List of locations (including HQ)
  * Distance/time matrix between locations
  * Service time required at each location
  * Time window constraints (earliest start, latest finish)
* Basic validation is performed to ensure required fields are present.

**2. Route Generation Using Multiple Heuristic Strategies**

Instead of relying on a single rule, the system generates multiple possible visit orders using different greedy strategies:

* **Nearest Neighbor Strategy**

  * Always selects the closest unvisited location from the current position.
  * Helps reduce travel distance and time.

* **Earliest Deadline First Strategy**

  * Sorts locations based on the earliest closing time of their time window.
  * Gives priority to locations that may close soon.

* **Shortest Service Time First Strategy**

  * Visits locations that require less service time first.
  * Helps complete more visits within limited time.

* **Adaptive Strategy (Dynamic Decision-Based)**

  * At each step, evaluates all remaining locations.
  * Considers:

    * Distance from current position
    * Expected arrival time
    * Time window constraints
    * Waiting time if arriving early
  * Assigns a score and chooses the best next location dynamically.

Each strategy produces one possible route.

**3. Time Simulation Engine**

For every generated route, the system simulates real-time execution:

At each location:

* Travel time from current location is added.
* Arrival time is calculated.
* Time window is checked:

  * If arrival is after latest allowed time → location is skipped.
  * If arrival is before earliest allowed time → waiting time is added.
  * If arrival is within the window → service starts immediately.
* Service time is added to total duration.
* Visit details are recorded.

After finishing all possible visits:

* Vehicle returns back to HQ.
* Return travel time is also included in total time.

**4. Best Route Selection**

After simulating all strategies, the final best route is selected using:

1. Maximum number of successfully visited locations
2. If tied → Minimum total travel time

This ensures:

* More locations are serviced
* Travel is still efficient

---

### Constraint Handling

The solution strictly respects the required constraints:

* A location is visited only if arrival time ≤ latest finish time.
* If early, the system waits until the allowed start time.
* If late, the location is skipped and recorded with a reason.
* Total time includes:

  * Travel time
  * Service time
  * Waiting time
  * Return to HQ

---

### Assumptions Made

* The route always starts and ends at HQ.
* Travel time is taken directly from the distance matrix.
* Service time is fixed per location.
* If arrival is early, the vehicle waits.
* If arrival is late, the location is skipped.
* Missing distance values are treated as very large (unreachable).
* HQ has no service time.
* Time starts from 0 at HQ.
* No traffic variations or dynamic travel changes are considered.
* Vehicle capacity constraints are not used (optional part not implemented).

---

### Why This Approach Was Chosen

* The routing problem with time windows is computationally complex.
* Instead of using advanced optimization libraries, the solution uses:

  * Multiple greedy strategies
  * Time-based simulation
  * Best-result comparison
* This keeps the implementation:

  * Simple
  * Fully manual
  * Easy to understand
  * Within the assignment rules
