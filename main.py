from parser_engine import ParserEngine
from graph_builder import GraphBuilder
from graph_solver import GraphSolver

import sys


def main(config_file: str) -> None:
    configs = ParserEngine(config_file).config

    builder = GraphBuilder(configs)
    graph, start_node, end_node = builder.build_graph()

    solver = GraphSolver(graph)
    result = solver.shortest_path(start_node, end_node)

    if result["path"]:
        print(f"Distance : {result['distance']}")
        print(f"Path     : {' -> '.join(result['path'])}")
    else:
        raise RuntimeError("No path found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config_file>")
        sys.exit(1)

    try:
        main(sys.argv[1])
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)