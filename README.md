 *This project has been created as part of the 42 curriculum by  eboulajd.*

 ---
 # Description
 ### General idea bout the Fly-in project
 Fly-in is project that contain allot of consepts, the main goal of this project is to make engin to manipulate the trafc of multiple dornes, input comme from config.txt.
 ### Config file
  config gile contain three parts first one is `nb_drones` parameter that should be at the begining of the file, if not the program should be stop and raise costom Error message.
 ```
 nb_drones: n => n is positive integer && it should be at the first line 
 ```
the second part is the parameters that contain three types: 
 ```
 coordinates/
 ├── start_hub:   start    (coordinates)  [Metadata]
 ├── hub:         name_1   (coordinates)  [Metadata]
 ├── hub:         name_2   (coordinates)  [Metadata]
 ├── ...          ...       ...           [Metadata]
 ├── hub:         name_n   (coordinates)  [Metadata]
 ├── end_hub:     goal     (coordinates)  [Metadata]
 ```
 so the type one is `start_hub` that contain the name of hub and the coordinates and also some Metadata, and it should be just one parameter named `start_hub` and if not the program must stop and raise costom message Error, the second type of parameters is `hub` so this is like a place that have name and coordinates and some metadata, this one is the zones that the drones may or may not pass throuit, the last type is like the first one, `end_hub` is parameter that contain also a name and coordinates and metadata and this one is the goal of all drones, so after starting from `start_hub`and pasing by all or some of `hub` zones the last station or the goal is `end_hub` zone.

 the last part is connection part:
 ```
 connection: start-hub_1    [metadata]
 connection: hub_1-hub_2    [metadata]
 connection: hub_1-hub_3    [metadata]
 connection: hub_3-goal     [metadata]
 ```
 and any line start with `#` is comment and should be skiped !
 ```
 #comment line that should be skiped !
 ```

 ### parsing part
 thsi part is wher we read form the config file line by line and if ther is any problem we raise Costom Error message that expalin the error and the line wher it's hapend.
 so at the parsing part i use Creational designe pattern espesialy `Factory Method` to create an object to work with it in the rest of the code.
 the class `FactoryEngin` takes the name of cofig file as argv parameter, the main method in this class is the `parse_file` method that take config file as parameter and return list,
 let's divin to this function deeply !
 firs thing is declare some parameters and flags that we will work with, 
 after opening the confing file i loop throuit, so at this pat i handel the comments first, than it normal conig lines, by cheking the key is valide for any if conndition in the for loop if ther is match and ther is not general problem in the config line it pass the line in to `create` method that in `ParserFactory`, so after puting the data in to parser variable we pass it as aparameter in to parse abstract method, the `ParserFactory` class use `create` class method that parse using a key, which each one is have a sepesial class and that's why we use the  `_parsers` dict to make it automated and avoid using if conditions, each class of those use simple algorithme so parse the line of code with simple algo so it returns a clean and well parsed config line, and also for parsing we make `BaseParser` that enhirit from `ABC` class, also i use `HubColor` class that enhirit from Enum, 
 combining all of this consepts and codes abd base on **Factory Method** i make this well structerd parsing.

 ### Graph building 
 At the part of graph builder the code is simple and clean, so we have one calss that do all the work, the class of `GraphBuilder` contain four simple methodes:
 
 `__init__`: that take the config as parameter, initialise the graph with empty dictionary, initialise start and end flags with None value.

`add_node`: that simply check if the hub name parameter if ther is not in the graph than it's add it as key and add two values config = None, also neghbhors empty list that will be fille with other hubs name later

`add_connection`: this function just add a connection between two nodes

`build_graph`: this is the main functin in the graph builder calss, it loops over every parsed object, and make the connetcions and hubs.

### Algorithm explanation
The graph is traversed using Dijkstra's shortest path algorithm, which computes the minimum-cost path from the start hub to the destination hub. Every hub is initially assigned an infinite distance, except the start hub, which begins with a distance of 0. At each iteration, the algorithm selects the unvisited hub with the smallest known distance and updates the distances of its neighboring hubs if a shorter path is found. The movement cost depends on the destination hub's zone type: normal hubs have a cost of 1, restricted hubs have a higher cost of 2, priority hubs have a lower cost of 0.9, and blocked hubs are ignored entirely since they cannot be traversed. Once the destination is reached (or no reachable hubs remain), the algorithm reconstructs the optimal path by following the recorded predecessors from the destination back to the start, producing the final shortest route.

### Simulation
The simulation executes the movement of all drones turn by turn, ensuring that every drone moves simultaneously while respecting the constraints of the environment. During each turn, the simulator attempts to advance every drone to the next hub on its precomputed shortest path. Before a movement is allowed, it verifies several conditions: the destination hub must not be blocked, drones entering a restricted hub must wait one turn before moving, the destination hub must not exceed its maximum drone capacity, and only one drone may use the same connection during a single turn. If all conditions are satisfied, the drone advances to the next hub, the occupancy of both hubs and the connection usage are updated, and the movement is recorded. This process repeats until every drone reaches the destination hub, producing a step-by-step simulation of all drone movements while enforcing zone and connection constraints.

# Example

### Example Input (`config.txt`)

```txt
# Easy Level 3: Basic capacity management
nb_drones: 4

start_hub: start 0 0 [color=green max_drones=4]
hub: bottleneck 1 0 [color=orange max_drones=2]
hub: wide_area 2 0 [color=blue max_drones=3]
end_hub: goal 3 0 [color=red max_drones=4]

connection: start-bottleneck [max_link_capacity=4]
connection: bottleneck-wide_area [max_link_capacity=4]
connection: wide_area-goal [max_link_capacity=4]
```

### Execution

```bash
make run
```

or

```bash
python3 main.py config.txt
```

### Expected Output

```txt
D1-bottleneck
D1-wide_area D2-bottleneck
D1-goal D2-wide_area D3-bottleneck
D2-goal D3-wide_area D4-bottleneck
D3-goal D4-wide_area
D4-goal
```

In the output, each line represents one simulation turn. Every entry has the format:

```text
D<drone_id>-<hub_name>
```

where `drone_id` identifies the drone and `hub_name` is the hub it occupies after moving during that turn. Multiple entries on the same line indicate drones moving simultaneously while respecting hub capacities and connection constraints.

## Visual Representation

The simulation uses colored terminal output to make the movement of drones easier to follow.

- 🟢 **Green**: Start hub
- 🔴 **Red**: End hub
- 🔵 **Blue**: Normal hub
- 🟠 **Orange**: Restricted hub
- 🟡 **Yellow**: Priority hub
- 🟣 **Purple**: Danger hub
- ⚫ **Black**: Blocked hub

Using different colors allows users to quickly identify hub types and better understand the simulation as drones move through the network.

# Instructions


### Requirements

- Python 3.10 or later
- `pip`
- `make`

### Installation

Install the project dependencies:

```bash
make install
```

### Execution

Run the simulation using the default configuration file (`config.txt`):

```bash
make run
```

### Debugging

Run the project with the Python debugger:

```bash
make debug
```

### Static Analysis

Run the required linting and type checking:

```bash
make lint
```

Run strict type checking:

```bash
make lint-strict
```

### Cleanup

Remove Python cache files and temporary directories:

```bash
make clean
```

 




---
# Resources

### documentations
[File handling](https://www.w3schools.com/python/python_file_handling.asp)\
[Python abc Module](https://www.w3schools.com/Python/ref_module_abc.asp)\
[Enum in python](https://www.geeksforgeeks.org/python/enum-in-python/)\
[Creational Design Patterns](https://refactoring.guru/design-patterns/creational-patterns)\
[Dijkstra algorithme](https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/)
