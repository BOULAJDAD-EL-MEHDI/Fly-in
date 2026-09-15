from dataclasses import dataclass
from base_parser import BaseParser
from parser_errors import NbDronesError


@dataclass
class NbDronesConfig:
    nb_drones: int


class NbDronesParser(BaseParser):

    def parse(self, line: str) -> NbDronesConfig:
        tokens = self._split_line(line)
        if len(tokens) != 2:
            raise NbDronesError("Invalid nb_drones format !")
        self._parse_key(tokens[0])
        nb_drones_value = self._parse_value(tokens[1])
        if nb_drones_value <= 0:
            raise NbDronesError("nb_drones must be greater than 0!")
        return NbDronesConfig(nb_drones=nb_drones_value)

    def _split_line(self, line: str) -> list[str]:
        return line.split(":", 1)

    def _parse_key(self, key: str) -> None:
        if key.strip().lower() != "nb_drones":
            raise NbDronesError("Invalid nb_drones key !")
        
    def _parse_value(self, value: str) -> int:
        try:
            return int(value.strip())
        except ValueError:
            raise NbDronesError("nb_drones must be integer!")