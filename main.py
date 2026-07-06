from parser_engine import ParserEngine
from graph_builder import GraphBuilder
from graph_solver import GraphSolver

import sys


def main(config_file: str) -> None:
    # Parse the configuration file
    configs = ParserEngine(config_file).config

    # Build the graph
    builder = GraphBuilder(configs)
    graph = builder.build_graph()

    # Create the solver
    solver = GraphSolver(graph)

    # Example: find the shortest path
    result = solver.shortest_path((0, 0), (5, 3))

    # Display the result
    if result["path"]:
        print(f"Distance : {result['distance']}")
        print(f"Path     : {result['path']}")
    else:
        print("No path found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config_file>")
        sys.exit(1)

    try:
        main(sys.argv[1])
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)