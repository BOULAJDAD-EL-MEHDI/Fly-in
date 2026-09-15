*This project has been created as part of the 42 curriculum by eboulajd.*

# Fly-in

**A Python command-line simulator for routing multiple drones through a graph with zone and connection constraints.**

Fly-in reads a text map, validates its hubs and connections, finds a lowest-cost route from the start to the destination, and simulates the drones moving along that route. Its terminal output shows each successful movement and the total number of turns.

The project brings together structured parsing, object-oriented design, graph representation, weighted shortest paths, and scheduling under capacity constraints. The implementation uses one route for every drone; it does not distribute traffic across alternative routes or guarantee the fewest turns for the entire fleet.

## Installation and usage

### Requirements

- **Python 3.10 or later**, for the type annotation syntax used in the source.
- **Make**, for the convenience commands below.
- **pip**, to install the packages listed in `requirements.txt`.

There is no compilation step. The simulator itself imports only the Python standard library and can run directly:

```sh
python3 main.py config.txt
python3 main.py maps/easy/01_linear_path.txt
```

To install the declared dependencies in an isolated environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
make install
```

`requirements.txt` lists `pydantic`, `flake8`, and `mypy`. Flake8 and mypy support development checks; Pydantic is currently not used by the code. Parsed records use standard-library dataclasses and explicit validation.

| Command | Purpose |
| --- | --- |
| `make run` | Run `main.py` with `config.txt`. |
| `make run CONFIG=maps/medium/03_priority_puzzle.txt` | Run another map. |
| `make debug CONFIG=config.txt` | Open the program and selected map in Python's `pdb` debugger. |
| `make lint` | Run Flake8, then mypy if Flake8 succeeds. |
| `make clean` | Remove Python bytecode and mypy/pytest cache directories beneath the project. |

The CLI requires exactly one map filename. Errors encountered while parsing, opening the file, finding a route, or simulating are printed, and the process exits with status `1`. Calling the program with the wrong number of arguments prints its usage message.

### Example output

For the supplied `maps/easy/01_linear_path.txt`:

```sh
python3 main.py maps/easy/01_linear_path.txt
```

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
4
```

Each entry is `D<drone_id>-<destination_hub>`. Entries on the same line belong to the same simulation turn. Drones that stay in place have no entry. A turn spent entirely waiting is represented by a blank line, and the final integer includes those turns. The example omits ANSI escape sequences used to color hub names.

## Map format

```text
# Comments and blank lines are ignored.
nb_drones: 3

start_hub: start 0 0 [color=green]
hub: corridor 1 0 [zone=restricted color=orange max_drones=2]
end_hub: goal 2 0 [color=red]

connection: start-corridor [max_link_capacity=2]
connection: corridor-goal
```

### Records and ordering

| Record | Syntax | Meaning |
| --- | --- | --- |
| Drone count | `nb_drones: N` | Positive integer; must be the first meaningful line. |
| Start | `start_hub: NAME X Y [metadata]` | Exactly one departure hub. |
| Intermediate hub | `hub: NAME X Y [metadata]` | A possible waypoint. |
| Destination | `end_hub: NAME X Y [metadata]` | Exactly one arrival hub, distinct from the start. |
| Connection | `connection: NAME1-NAME2 [metadata]` | An undirected link between two already declared hubs. |

Use a space after the colon in hub and connection records. Hub names are unique and case-sensitive. They cannot contain whitespace or `-`, `[`, `]`, or `=`. Coordinates are integer pairs; negative values are accepted. Coordinates are stored as map metadata and do not determine connectivity, distance, or travel time.

`#` starts a comment, including after a record. Metadata is optional and occupies a single trailing bracket block. Inside it, use whitespace-separated `key=value` pairs without spaces around `=`. An empty block, duplicate keys, unknown attributes, or malformed brackets are rejected.

### Hub metadata

| Attribute | Default | Behavior |
| --- | --- | --- |
| `zone` | Unspecified, treated as `normal` | Controls route cost and restricted/blocked movement rules. |
| `max_drones` | `1` | Positive occupancy limit for intermediate hubs. |
| `color` | No foreground color | Controls terminal display only. |

All drones initially occupy the start, regardless of its `max_drones` value. The destination accepts all arriving drones, regardless of its capacity. These endpoint exceptions allow the fleet to depart and finish even when endpoint metadata uses the default capacity.

Supported zones:

| Zone | Cost of entering it during pathfinding | Simulation behavior |
| --- | --- | --- |
| `normal` | `1` | Move in one turn when capacity allows. |
| `priority` | `0.9` | Move in one turn; the lower cost favors this zone during route selection. |
| `restricted` | `2` | Wait one turn before entering; capacity contention may add further delay. |
| `blocked` | Not traversable | Excluded from routes; a blocked start has no valid route. |

Color and zone are independent: `color=orange` alone does not make a hub restricted, and `color=black` alone does not block it. The supported lowercase colors are:

```text
red green blue yellow orange purple pink black white gray brown
cyan magenta lime navy teal olive maroon silver gold darkred
violet crimson
```

### Connection metadata

`max_link_capacity` is a positive integer, defaulting to `1`. It limits the number of drones using that connection in one turn. The same link is identified in both directions, so its capacity is shared.

Self-loops, references to undeclared hubs, and duplicate connections—including reversed duplicates—are rejected. A syntactically valid map can still have no traversable route; pathfinding detects that separately.

## How the project works

```text
Map file
   |
   v
ParserEngine -> ParserFactory -> specialized BaseParser implementations
   |                            (validated dataclass records)
   v
GraphBuilder -> undirected adjacency graph with hub and link metadata
   |
   v
GraphSolver -> one weighted shortest path
   |
   v
SimulationEngine -> drone states, occupancy, per-turn link usage
   |
   v
main.py -> colored movement lines and total turns
```

### 1. Parsing, validation, and OOP

`ParserEngine` reads the file with a `with open(...)` context manager, strips comments, and dispatches each meaningful record. It also checks rules spanning multiple lines: required entries, unique hub names, known connection endpoints, and duplicate links. Sets provide membership checks for declared hubs and connections.

`ParserFactory` holds a dictionary mapping record keys to parser classes. Its class method constructs the corresponding parser. Each parser implements the abstract `BaseParser.parse()` interface and returns its own dataclass, such as `HubConfig` or `ConnectionConfig`. This separates parser selection from each record's parsing rules.

`BaseParser._parse_attributes()` handles the shared bracket and key/value syntax. Specialized parsers validate integer coordinates, positive capacities, permitted zone values, and colors. `HubColor`, an enum, restricts color values to the supported set. Type annotations describe record fields and parser interfaces; runtime correctness comes from these explicit checks, since dataclasses do not enforce field types themselves.

Custom exceptions distinguish record-specific errors from file-level inconsistencies. The CLI catches exceptions at its entry point. Error messages describe the problem but currently do not include line numbers.

### 2. Graph representation and data structures

`GraphBuilder` constructs a dictionary keyed by hub name. Each node holds:

- `config`: the hub's parsed dataclass, including its zone, coordinates, color, and capacity.
- `neighbors`: a list of connected hub names.
- `link_capacity`: a dictionary mapping each neighbor to the connection's capacity.

Each connection adds adjacency and capacity information at both endpoints. This represents an undirected graph, including branches, cycles, and dead ends. The graph occupies **O(V + E)** space, where `V` is the number of hubs and `E` is the number of connections.

The parser requires both endpoints before a connection can be built. That validation ensures the graph builder receives links to known hubs.

### 3. Weighted pathfinding with Dijkstra's algorithm

`GraphSolver.shortest_path()` maintains three structures:

- `distances`: the best known cost to each hub, initially infinity except for the start at zero.
- `previous`: the predecessor used to reach each hub at its best known cost.
- `visited`: the hubs whose minimum distance has been settled.

At each iteration, it scans the graph to select the unvisited hub with the smallest distance. For each accessible neighbor, it adds the cost of entering that neighbor. If the candidate cost is lower, it updates both the distance and predecessor. This update is called **edge relaxation**.

All traversable costs are positive, allowing Dijkstra's greedy selection to settle minimum distances. The search stops when it reaches the destination or no reachable unvisited hub remains. It reconstructs the route by following predecessors backward from the destination, then reversing that list. It returns an empty list when no route exists.

This implementation uses a linear scan to select the next hub, giving **O(V² + E)** time and **O(V)** auxiliary space. Equal-cost alternatives retain the first predecessor discovered, with traversal order following graph insertion order.

The route cost is based on zone types. Hub and connection capacities affect the later simulation, not path selection. Consequently, the cheapest route for one drone may not provide the fastest completion time for many drones.

### 4. Turn-based scheduling and state management

`main.py` assigns the same computed path to every drone. Each drone has a dictionary containing its ID, path reference, current path index, restricted-zone wait flag, and completion flag. The path is shared without modification; each drone advances its own index.

During each turn, the simulator visits drones in ascending ID order and attempts at most one move per drone:

1. Skip finished drones.
2. Read the next hub and reject a blocked destination.
3. For a restricted hub, record the first waiting turn before attempting entry on a later turn.
4. Check the next hub's occupancy, except at the final destination.
5. Check the connection's remaining capacity for this turn.
6. On success, update occupancy and link usage, advance the index, clear the wait flag, and mark arrivals as finished.

`zone_count` persists across turns. `connection_count` resets each turn and uses a sorted endpoint tuple as its key, so `A-B` and `B-A` consume the same resource. Occupancy changes immediately after each successful move: a hub vacated by an earlier drone can accept a later drone in that turn.

This is a **single-threaded, deterministic simulation**. The output groups movements into logical turns, while the implementation resolves them sequentially. It uses no threads, mutexes, or condition variables.

A turn without movement is allowed when a drone has just begun its required wait. Otherwise, unfinished drones with no progress cause a simulation deadlock error. Tracking a newly started wait prevents an old wait flag from keeping a stalled simulation alive indefinitely.

The loop performs one pass over the drones per turn: **O(T × D)** simulation work for `T` turns and `D` drones, excluding output formatting. It accumulates the complete output list before printing. Python manages object memory; file handles are closed by the context manager, including on parsing errors.

## Technical challenges and learning outcomes

The central engineering challenge is keeping input validity, route choice, and movement feasibility consistent across the pipeline:

- **Validation across records:** a valid-looking connection is only usable if both endpoints exist, and duplicate names would otherwise merge distinct hub definitions in the graph.
- **Traversal through cycles and branches:** distance relaxation, a visited set, and predecessor reconstruction find a route without getting trapped in graph loops or dead ends.
- **Two kinds of capacity:** hub occupancy lasts across turns, while link usage is a resource budget renewed every turn.
- **Restricted-zone state:** the wait flag belongs to the next move and must reset after that move, so every restricted hub imposes its own delay.
- **Progress versus deadlock:** an intentional waiting turn must count toward elapsed time without being mistaken for a permanent stall.

These problems develop practical skills in decomposing a program into cooperating classes, designing structured records, validating untrusted text input, implementing weighted graph search, and reasoning about state transitions and resource constraints. They also illustrate the distinction between finding a shortest route and optimizing a complete fleet schedule.

## Project structure

```text
Fly-in/
├── main.py                  # CLI and pipeline orchestration
├── base_parser.py           # Abstract interface and metadata parsing
├── parser_factory.py        # Record key -> parser class registry
├── parser_engine.py         # File parsing and cross-record validation
├── parser_errors.py         # Custom exception classes
├── nb_drones_parser.py      # Drone count parser and dataclass
├── start_hub_parser.py      # Start hub parser and dataclass
├── hub_parser.py            # Intermediate hub parser and dataclass
├── end_hub_parser.py        # Destination parser and dataclass
├── connection_parser.py     # Connection parser and dataclass
├── graph_builder.py         # Adjacency graph construction
├── graph_solver.py          # Weighted Dijkstra search
├── simulation_engine.py     # Drone movement and turn accounting
├── colors.py                # Color enum and ANSI formatting
├── config.txt               # Default map
├── maps/
│   ├── easy/                # 3 maps: linear path, fork, capacity
│   ├── medium/              # 3 maps: dead ends, cycle, priorities
│   ├── hard/                # 3 maps: maze, capacity, combined challenges
│   ├── challenger/          # 1 larger stress map
│   └── README.md            # Map descriptions and challenge targets
├── requirements.txt
├── Makefile
└── README.md
```

## Testing

The repository provides map fixtures and static-analysis commands; it does not contain a committed automated test suite.

### Run the supplied maps

```sh
python3 -B main.py config.txt
for map in maps/easy/*.txt maps/medium/*.txt maps/hard/*.txt maps/challenger/*.txt; do
    echo "$map"
    python3 -B main.py "$map" || break
done
```

`-B` avoids generating bytecode. During this review, the default configuration and all ten supplied maps completed on Python 3.13.15. The linear example takes **4 turns**, the basic-capacity map takes **4 turns**, and the challenger map takes **67 turns**. The targets in `maps/README.md` are challenge goals, not guarantees of this implementation.

Focused temporary regression checks cover link capacities, hub occupancy, repeated restricted-zone waits, idle-turn accounting, duplicate hub names, malformed records, and path selection around priority and blocked zones. These checks were run during the review and are not included as a repository test command.

### Static analysis

```sh
make lint
```

The existing source has style and typing diagnostics, so this command is not currently a passing check. Flake8 failures stop the Make recipe before mypy runs. To run the configured type check independently:

```sh
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
    --disallow-untyped-defs --check-untyped-defs
```

`lint-strict` is listed in `.PHONY` but has no recipe; it performs no checks.

## Resources

Useful links to learn the concepts used in Fly-in.

### Python and object-oriented programming

- [Classes and objects](https://docs.python.org/3/tutorial/classes.html) — the basics of OOP in Python.
- [Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance) — sharing behavior between parser classes.
- [Abstract classes](https://docs.python.org/3/library/abc.html) — defining the common `BaseParser` interface.
- [Class methods](https://docs.python.org/3/library/functions.html#classmethod) — how `ParserFactory.create()` works.
- [Dataclasses](https://docs.python.org/3/library/dataclasses.html) — storing parsed configuration records.
- [Enums](https://docs.python.org/3/library/enum.html) — representing the supported hub colors.
- [Type hints](https://docs.python.org/3/library/typing.html) — describing expected types in the code.
- [Modules and imports](https://docs.python.org/3/tutorial/modules.html) — connecting the project's Python files.

### Data structures and memory

- [Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists) — storing neighbors, paths, and drones.
- [Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) — storing the graph, distances, and drone states.
- [Sets](https://docs.python.org/3/tutorial/datastructures.html#sets) — tracking visited hubs and detecting duplicates.
- [Tuples](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) — storing coordinates and connection endpoints.
- [Objects, references, and memory](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types) — understanding shared objects and automatic memory management.

### Parsing and error handling

- [Reading files and using `with`](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files) — reading a map and closing the file safely.
- [String methods](https://docs.python.org/3/library/stdtypes.html#string-methods) — splitting records and removing comments and whitespace.
- [Exceptions](https://docs.python.org/3/tutorial/errors.html) — reporting invalid input and handling failures.
- [Custom exceptions](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions) — creating project-specific parsing errors.
- [Command-line arguments](https://docs.python.org/3/library/sys.html#sys.argv) — getting the map filename from the command line.

### Graphs and algorithms

- [Undirected graphs and adjacency lists](https://algs4.cs.princeton.edu/41graph/) — representing hubs and their connections.
- [Dijkstra's algorithm and shortest paths](https://algs4.cs.princeton.edu/44sp/) — weighted routes, edge relaxation, and path reconstruction.
- [Algorithm complexity](https://algs4.cs.princeton.edu/14analysis/) — understanding running time and memory costs.

### Development tools and terminal output

- [Python debugger (`pdb`)](https://docs.python.org/3/library/pdb.html) — stepping through the program.
- [Flake8](https://flake8.pycqa.org/en/latest/) — checking Python style and common mistakes.
- [Mypy](https://mypy.readthedocs.io/en/stable/getting_started.html) — checking type annotations.
- [Virtual environments and pip](https://docs.python.org/3/tutorial/venv.html) — installing dependencies in an isolated environment.
- [ANSI terminal colors](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html) — the escape sequences used to color hub names.

### Examples in this project

- [Parser factory](parser_factory.py) — choosing a parser using a class registry.
- [Input validation](parser_engine.py) — checking names, required records, and connections.
- [Turn-based scheduling](simulation_engine.py) — tracking movement, waiting, capacities, and deadlocks.
- [Challenge maps](maps/README.md) — examples of the graph problems the simulator handles.
