class SimulationEngine:
    """Simulates drone movement turn by turn."""

    def __init__(self, graph, nb_drones, start, end, shortest_paths):
        """
        Initialize the simulation.
        
        Args:
            graph: The graph structure with nodes and connections
            nb_drones: Total number of drones to simulate
            start: Starting zone name
            end: Ending zone name
            shortest_paths: List of shortest paths (one per drone)
        """
        self.graph = graph
        self.nb_drones = nb_drones
        self.start = start
        self.end = end
        self.shortest_paths = shortest_paths

        # Track each drone's state
        self.drones = self._initialize_drones()

        # Track zone occupancy (how many drones are currently in each zone)
        self.zone_drones = {}

        # Track restricted zone entry (drones waiting to enter restricted zones)
        self.restricted_waiting = {}

    def _initialize_drones(self):
        """Create a drone for each path."""
        drones = []
        for drone_id in range(self.nb_drones):
            drones.append({
                'id': drone_id,
                'path': self.shortest_paths[drone_id],
                'position': 0,  # Index in the path
                'current_zone': self.start,
                'finished': False,
                'waiting_for_restricted': False,  # True if waiting to enter restricted zone
            })
        return drones

    def _get_zone_config(self, zone_name):
        """Get the configuration object for a zone."""
        return self.graph[zone_name].get('config')

    def _get_zone_capacity(self, zone_name):
        """Get the max drones allowed in a zone."""
        config = self._get_zone_config(zone_name)
        if config is None:
            return 1  # Default capacity
        return config.max_drones

    def _get_zone_type(self, zone_name):
        """Get the zone type (normal, restricted, priority, blocked)."""
        config = self._get_zone_config(zone_name)
        if config is None or config.zone is None:
            return 'normal'
        return config.zone

    def _count_drones_in_zone(self, zone_name):
        """Count how many drones are currently in a zone."""
        if zone_name not in self.zone_drones:
            self.zone_drones[zone_name] = 0
        return self.zone_drones[zone_name]

    def _get_connection_capacity(self, from_zone, to_zone):
        """Get the max drones that can use a connection between two zones."""
        for neighbor in self.graph[from_zone].get('neighbors', []):
            if neighbor == to_zone:
                # Find the connection config
                for config in self.graph[from_zone].get('connections', []):
                    if config['to'] == to_zone:
                        return config.get('capacity', 1)
        return 1  # Default capacity

    def _count_drones_using_connection(self, from_zone, to_zone):
        """Count how many drones are using a specific connection this turn."""
        count = 0
        for drone in self.drones:
            if drone['finished']:
                continue
            # Check if this drone is moving on this connection
            if drone['current_zone'] == from_zone:
                next_zone = self._get_next_zone(drone)
                if next_zone == to_zone:
                    count += 1
        return count

    def _get_next_zone(self, drone):
        """Get the next zone a drone wants to move to."""
        if drone['finished']:
            return None
        if drone['position'] + 1 >= len(drone['path']):
            return None
        return drone['path'][drone['position'] + 1]

    def _can_enter_zone(self, drone, next_zone):
        """Check if a drone can enter a zone this turn."""
        zone_type = self._get_zone_type(next_zone)

        # Blocked zones cannot be entered
        if zone_type == 'blocked':
            return False

        # Check zone capacity
        current_in_zone = self._count_drones_in_zone(next_zone)
        capacity = self._get_zone_capacity(next_zone)
        if current_in_zone >= capacity:
            return False

        # Restricted zones: check if drone has already waited
        if zone_type == 'restricted':
            if not drone.get('waiting_for_restricted', False):
                # First time trying to enter: must wait one turn
                return False

        return True

    def _can_use_connection(self, drone, from_zone, to_zone):
        """Check if a drone can use a connection this turn."""
        # Count drones already using this connection in this turn
        using = self._count_drones_using_connection(from_zone, to_zone)
        capacity = self._get_connection_capacity(from_zone, to_zone)
        return using < capacity

    def _move_drone(self, drone):
        """Try to move a drone one step forward."""
        if drone['finished']:
            return False

        # Check if we've reached the end
        if drone['current_zone'] == self.end:
            drone['finished'] = True
            return False

        # Get the next zone in the path
        next_zone = self._get_next_zone(drone)
        if next_zone is None:
            drone['finished'] = True
            return False

        zone_type = self._get_zone_type(next_zone)

        # Handle restricted zones
        if zone_type == 'restricted':
            if not drone.get('waiting_for_restricted', False):
                # Mark as waiting, but don't move yet
                drone['waiting_for_restricted'] = True
                return False
            # Second turn: try to actually move
            drone['waiting_for_restricted'] = False

        # Check if we can enter the zone and use the connection
        if not self._can_enter_zone(drone, next_zone):
            return False

        if not self._can_use_connection(drone, drone['current_zone'], next_zone):
            return False

        # Move the drone
        self.zone_drones[drone['current_zone']] -= 1
        drone['position'] += 1
        drone['current_zone'] = next_zone
        if next_zone not in self.zone_drones:
            self.zone_drones[next_zone] = 0
        self.zone_drones[next_zone] += 1
        return True

    def simulate(self):
        """Run the simulation and return output."""
        output = []

        # Initialize zones
        self.zone_drones[self.start] = self.nb_drones

        turn = 0
        while True:
            turn += 1

            # Try to move all drones in this turn
            moved_this_turn = []
            for drone in self.drones:
                if self._move_drone(drone):
                    moved_this_turn.append(drone['id'])

            # Print output for this turn
            if moved_this_turn:
                output.append(f"Turn {turn}: {' '.join(map(str, sorted(moved_this_turn)))}")

            # Check if all drones are finished
            if all(drone['finished'] for drone in self.drones):
                break

            # Safety check to avoid infinite loops
            if turn > 1000:
                break

        return output
