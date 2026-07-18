from parser_factory import ParserFactory
from parser_errors import ParsingKeyError
from typing import Any


class ParserEngine:

    def __init__(self, config_path: str) -> None:
        self.config = self.parse_file(config_path)

    def parse_file(self, file_path: str) -> list[Any]:
        config = []
        defined_zones: set[str] = set()
        connections: set[tuple[str, str]] = set()
        nb_drones_seen = False
        start_hub_seen = False
        end_hub_seen = False
        start_name: str | None = None
        end_name: str | None = None
        first_meaningful_line = False

        with open(file_path) as file:
            for raw_line in file:
                line = raw_line.split("#", 1)[0].strip()
                if not line:
                    continue

                first_meaningful_line = True
                key = line.split(":", 1)[0].lower()
                if not nb_drones_seen:
                    if key != "nb_drones":
                        raise ParsingKeyError("nb_drones must be the first meaningful line !")

                parser = ParserFactory.create(key)
                obj = parser.parse(line)

                if key == "nb_drones":
                    if nb_drones_seen:
                        raise ParsingKeyError("Duplicate nb_drones entry !")
                    nb_drones_seen = True
                    config.append(obj)
                    continue

                if key == "start_hub":
                    if start_hub_seen:
                        raise ParsingKeyError("Duplicate start_hub entry !")
                    start_hub_seen = True
                    parts = line.split()
                    if len(parts) < 3:
                        raise ParsingKeyError("Invalid start_hub format !")
                    start_name = parts[1].strip()
                    if not start_name:
                        raise ParsingKeyError("Invalid start_hub name !")
                    defined_zones.add(start_name)
                    config.append(obj)
                    continue

                if key == "end_hub":
                    if end_hub_seen:
                        raise ParsingKeyError("Duplicate end_hub entry !")
                    end_hub_seen = True
                    parts = line.split()
                    if len(parts) < 3:
                        raise ParsingKeyError("Invalid end_hub format !")
                    end_name = parts[1].strip()
                    if not end_name:
                        raise ParsingKeyError("Invalid end_hub name !")
                    if start_name is not None and start_name == end_name:
                        raise ParsingKeyError("start_hub and end_hub are the same zone !")
                    defined_zones.add(end_name)
                    config.append(obj)
                    continue

                if key == "hub":
                    zone_name = line.split()[1].strip()
                    if not zone_name:
                        raise ParsingKeyError("Invalid zone name !")
                    if zone_name in defined_zones:
                        raise ParsingKeyError("Duplicate zone name !")
                    defined_zones.add(zone_name)
                    config.append(obj)
                    continue

                if key == "connection":
                    first_zone, second_zone = obj.connection # type: ignore[attr-defined]
                    if first_zone not in defined_zones:
                        raise ParsingKeyError("Connection from unknown zone !")
                    if second_zone not in defined_zones:
                        raise ParsingKeyError("Connection to unknown zone !")
                    if first_zone == second_zone:
                        raise ParsingKeyError("Self-loop connection !")
                    connection_pair = (first_zone, second_zone)
                    reverse_pair = (second_zone, first_zone)
                    if connection_pair in connections or reverse_pair in connections:
                        raise ParsingKeyError("Duplicate connection !")
                    connections.add(connection_pair)
                    config.append(obj)
                    continue

                config.append(obj)

        if not first_meaningful_line:
            raise ParsingKeyError("Empty configuration file !")

        if not nb_drones_seen or not start_hub_seen or not end_hub_seen:
            raise ParsingKeyError("Missing required configuration entries !")

        return config
