import argparse
import sys
import os
import json

# classes to store data
class SimulationResult:
    def __init__(self, route):
        self.route = route
        self.total_travel_time = 0.0
        self.total_service_time = 0.0
        self.total_idle_time = 0.0
        self.visited_locations = []
        self.skipped_locations = {}
        self.visit_details = []

class SimulationState:
    def __init__(self, unvisited):
        self.current_time = 0.0
        self.current_location = 'HQ'
        self.visited_locations = []
        self.unvisited_locations = unvisited
        self.skipped_locations = {}
        self.total_travel_time = 0.0
        self.total_service_time = 0.0
        self.total_idle_time = 0.0
        self.visit_details = []

# read input file
def parse_input(file_path):
    if not os.path.exists(file_path):
        print("Error: file not found")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            required = ['locations', 'distance', 'service_time', 'time_window']
            for field in required:
                if field not in data:
                    print(f"Missing {field} in input")
                    return None
            return data
        except Exception as e:
            print(f"Failed to load json: {e}")
            return None

def get_output_filename(input_path):
    base = os.path.basename(input_path)
    name, _ = os.path.splitext(base)
    if name.startswith('input'):
        return name.replace('input', 'output') + ".txt"
    return "output_" + name + ".txt"

# simulation engine
class TimeSimulationEngine:
    def __init__(self, data):
        self.locations_list = data.get('locations', [])
        self.distances = data.get('distance', {})
        self.service_times = data.get('service_time', {})
        self.time_windows = data.get('time_window', {})

    def run_simulation(self, route_list):
        state = SimulationState(list(route_list))
        state.current_location = 'HQ'
        state.current_time = 0.0
        
        for next_loc in route_list:
            # check if distance exists
            if state.current_location in self.distances:
                dist = self.distances[state.current_location].get(next_loc, 999999)
            else:
                dist = 999999
            
            arrive_time = state.current_time + dist
            
            window = self.time_windows.get(next_loc, [0, 999999])
            start_time = float(window[0])
            end_time = float(window[1])
            
            wait = 0.0
            start = arrive_time
            skip = False
            reason = ""

            if arrive_time > end_time:
                skip = True
                # too late
                reason = f"Arrived at {round(arrive_time, 2)}, latest allowed {round(end_time, 2)}"
            elif arrive_time < start_time:
                wait = start_time - arrive_time
                state.total_idle_time += wait
                start = start_time
            else:
                start = arrive_time

            if skip:
                state.skipped_locations[next_loc] = reason
                continue

            service = self.service_times.get(next_loc, 0)
            finish = start + service
            
            state.visit_details.append({
                'location': next_loc,
                'arrival': arrive_time,
                'wait': wait,
                'start': start,
                'service': service,
                'finish': finish
            })

            state.total_travel_time += dist
            state.total_service_time += service
            state.visited_locations.append(next_loc)
            state.current_time = finish
            state.current_location = next_loc

        #go back to HQ
        if state.current_location in self.distances:
            to_hq = self.distances[state.current_location].get('HQ', 0)
        else:
            to_hq = 0
        state.total_travel_time += to_hq
        state.current_time += to_hq
        
        res = SimulationResult(['HQ'] + state.visited_locations + ['HQ'])
        res.total_travel_time = state.total_travel_time
        res.total_service_time = state.total_service_time
        res.total_idle_time = state.total_idle_time
        res.visited_locations = state.visited_locations
        res.skipped_locations = state.skipped_locations
        res.visit_details = state.visit_details
        return res

#strategies
class RouteStrategies:
    def __init__(self, data):
        self.locations = []
        for loc in data.get('locations', []):
            if loc != 'HQ':
                self.locations.append(loc)
        self.distances = data.get('distance', {})
        self.service_times = data.get('service_time', {})
        self.time_windows = data.get('time_window', {})

    def _sort_locations(self, locs, key_func):
        return sorted(locs, key=key_func)

    # pick nearest location each time
    def get_nearest_neighbor_route(self):
        unvisited = list(self.locations)
        current = 'HQ'
        route = []
        while len(unvisited) > 0:
            closest = None
            min_dist = 999999.0
            for loc in unvisited:
                d = self.distances[current].get(loc, 999999.0)
                if d < min_dist:
                    min_dist = d
                    closest = loc
            if closest:
                route.append(closest)
                unvisited.remove(closest)
                current = closest
            else:
                break
        return route

    # sort by deadline
    def get_earliest_deadline_first_route(self):
        locs = list(self.locations)
        return self._sort_locations(locs, lambda loc: self.time_windows.get(loc, [0, 999999])[1])

    # sort by service time
    def get_shortest_service_time_first_route(self):
        locs = list(self.locations)
        return self._sort_locations(locs, lambda loc: self.service_times.get(loc, 0))

def select_best_route(results):
    best_strategy = None
    max_visited = -1
    min_travel_time = 999999.0
    
    for name in results:
        res = results[name]
        count = len(res.visited_locations)
        travel = res.total_travel_time
        
        # pick route with most visits
        if count > max_visited:
            max_visited = count
            min_travel_time = travel
            best_strategy = name
            
        # if same visits then pick shorter time
        elif count == max_visited:
            if travel < min_travel_time:
                min_travel_time = travel
                best_strategy = name
                
    return best_strategy

#output process
def generate_result_file(best_result, strategy_name, output_file):
    folder = os.path.dirname(output_file)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("--- ROUTE OPTIMIZATION RESULT ---\n")
        f.write("Strategy: " + strategy_name + "\n\n")
        f.write("Best Route:\n")
        f.write(" -> ".join(best_result.route) + "\n\n")
        f.write("Total Travel Time:  " + str(round(best_result.total_travel_time, 2)) + "\n")
        f.write("Total Service Time: " + str(round(best_result.total_service_time, 2)) + "\n")
        f.write("Total Idle Time:    " + str(round(best_result.total_idle_time, 2)) + "\n")
        total_dur = best_result.total_travel_time + best_result.total_service_time + best_result.total_idle_time
        f.write("Total Duration:     " + str(round(total_dur, 2)) + "\n\n")
        f.write("Visited Locations:\n")
        for v in best_result.visit_details:
            line = " - " + v['location'] + ": "
            line += "Arrival=" + str(round(v['arrival'], 2)) + ", "
            line += "Wait=" + str(round(v['wait'], 2)) + ", "
            line += "Start=" + str(round(v['start'], 2)) + ", "
            line += "Service=" + str(round(v['service'], 2)) + ", "
            line += "Finish=" + str(round(v['finish'], 2)) + "\n"
            f.write(line)
        f.write("\n")
        f.write("Skipped Locations:\n")
        if not best_result.skipped_locations:
            f.write(" None\n")
        else:
            for loc in best_result.skipped_locations:
                reason = best_result.skipped_locations[loc]
                f.write(" - " + loc + ": " + reason + "\n")

def print_summary(best_result, strategy_name):
    print("\n--- Summary ---")
    print("Best Strategy: " + strategy_name)
    print("Route: " + " -> ".join(best_result.route))
    print("Visited: " + str(len(best_result.visited_locations)))
    print("Time: " + str(round(best_result.total_travel_time, 2)))
    print("---------------\n")

# main program
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input JSON file (required)")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    
    print("Reading file: " + args.input)
    data = parse_input(args.input)
    if not data:
        return

    output_file = args.output
    if output_file is None:
        name = get_output_filename(args.input)
        output_file = os.path.join("outputs", name)
    
    strategies = RouteStrategies(data)
    routes = {
        "Nearest Neighbor": strategies.get_nearest_neighbor_route(),
        "Earliest Deadline": strategies.get_earliest_deadline_first_route(),
        "Shortest Service": strategies.get_shortest_service_time_first_route()
    }
    
    engine = TimeSimulationEngine(data)
    all_results = {}
    for key in routes:
        all_results[key] = engine.run_simulation(routes[key])
    
    best_name = select_best_route(all_results)
    best_result = all_results[best_name]
    
    print_summary(best_result, best_name)
    generate_result_file(best_result, best_name, output_file)
    print("Done. Saved to " + output_file)

if __name__ == "__main__":
    main()
