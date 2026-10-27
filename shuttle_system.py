"""Campus shuttle timetable and fleet tracker.

Logs passenger counts per trip, works out average loads, flags under-used
routes and syncs the fleet data to ``fleet.json``.
"""
import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip for a route and append an entry to the log list.

    Raises ValueError for an unknown route or an invalid passenger count
    (it must be a non-negative integer).
    """
    if logs is None:
        logs = []
    if route_id not in routes:
        raise ValueError(f"unknown route: {route_id}")
    if (not isinstance(passenger_count, int)
            or isinstance(passenger_count, bool)
            or passenger_count < 0):
        raise ValueError(f"invalid passenger count: {passenger_count!r}")
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Delete a route and its trip history."""
    del routes[route_id]


def average_load(route_id):
    """Return the average passengers per trip for a route.

    Raises ValueError if the route does not exist or has no trips yet.
    """
    if route_id not in routes:
        raise ValueError(f"unknown route: {route_id}")
    trips = routes[route_id]["trips"]
    if not trips:
        raise ValueError(f"no trips logged for {route_id}")
    return sum(trips) / len(trips)


def underused_routes():
    """Return the ids of routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id, route in routes.items():
        if route["trips"] and average_load(route_id) < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver(route_id):
    """Pick a driver for an existing route."""
    if route_id not in routes:
        raise ValueError(f"unknown route: {route_id}")
    return secrets.choice(DRIVERS)


def sync_fleet_data(file="fleet.json"):
    """Write the current route data to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(routes, handle)


def main():
    """Run the demo: log trips, report loads, sync data and look up a route."""
    sample_trips = [("R1", 32), ("R1", 28), ("R2", 4), ("R2", -6),
                    ("R3", "full")]
    for trip_route, count in sample_trips:
        try:
            add_trip_log(trip_route, count)
        except ValueError as err:
            print("Rejected trip:", err)
    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("No such route:", choice)
    try:
        print("R3 average:", average_load("R3"))
    except ValueError as err:
        print("R3 average unavailable:", err)


if __name__ == "__main__":
    main()
