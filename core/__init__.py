from parsers import nb_drones_parser
from parsers import start_hub_parser
from parsers import end_hub_parser
from parsers import hub_parser
from parsers import connection_parser
from typing import List


class ConfigError(Exception):
    pass


__all__ = ["nb_drones_parser",
           "start_hub_parser",
           "end_hub_parser",
            "hub_parser",
            "connection_parser"]