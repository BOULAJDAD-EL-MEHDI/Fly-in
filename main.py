import sys

from parser_engine import ParserEngine
from graph_builder import GraphBuilder
from graph_solver import GraphSolver
from simulation_engine import SimulationEngine


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <config_file>")
        return

    configs = ParserEngine(sys.argv[1]).config

    graph, start, end = GraphBuilder(configs).build_graph()

    solver = GraphSolver(graph)
    path = solver.shortest_path(start, end)

    nb_drones = next(c.nb_drones for c in configs if hasattr(c, "nb_drones"))

    paths = [path for _ in range(nb_drones)]

    simulation = SimulationEngine(
        graph,
        nb_drones,
        start,
        end,
        paths,
    )


    # total_turns = len(simulation.simulate())
    # print(f"Total turns: {total_turns}")

    
    
    for line in simulation.simulate():
        print(line)


if __name__ == "__main__":
    main()