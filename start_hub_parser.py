from dataclasses import dataclass
from typing import Tuple
from base_parser import BaseParser
from colors import HubColor
from parser_errors import StartHubError


@dataclass
class StartHubConfig:
    start_hub: Tuple[int, int]
    color: HubColor
    max_drones: int = 1


class StartHubParser(BaseParser):

    def parse(self, line: str) -> StartHubConfig:
        tokens = self._split_line(line)
        self._key_validation(tokens[0])
        coordinates = self._coordinates_validation(tokens)
        attributes = self._parse_attributes(line)
        self._validate_attributes(attributes)
        color = self._color_validation(attributes)
        max_drones = self._max_drones_validation(attributes)
        return StartHubConfig(start_hub=coordinates, color=color, max_drones=max_drones)

    def _split_line(self, line: str) -> list[str]:
        line = line.strip()
        if line.endswith("]"):
            pos = line.rfind("[")
            if pos != -1:
                line = line[:pos].rstrip()
        return line.split()

    def _key_validation(self, key: str) -> None:
        start_key = key.lower().strip(":")
        if start_key != "start_hub":
            raise StartHubError("Invalid start_hub key !")
        
    def _coordinates_validation(self, tokens: list[str]) -> Tuple[int, int]:
        if len(tokens) < 4:
            raise StartHubError("Invalid start_hub format !")
        name = tokens[1]
        if any(char in name for char in "- []="):
            raise StartHubError("Invalid zone name !")
        try:
            x = int(tokens[2])
            y = int(tokens[3])
            return x, y
        except ValueError:
            raise StartHubError("Invalid coordinates type !")
    
    def _validate_attributes(self, attributes: dict) -> None:
        allowed_keys = {"color", "max_drones"}
        for key in attributes:
            if key not in allowed_keys:
                raise StartHubError("Unknown metadata key !")

    def _color_validation(self, attributes: dict) -> HubColor:
        color_value = attributes.get("color")
        if not color_value:
            return None
        try:
            return HubColor(color_value)
        except ValueError:
            raise StartHubError("Invalid color value !")
        
    def _max_drones_validation(self, attributes: dict) -> int:
        max_drones_str = attributes.get("max_drones", "1")
        try:
            max_drones = int(max_drones_str)
        except ValueError:
            raise StartHubError("Invalid max_drones value !")
        if max_drones <= 0:
            raise StartHubError("max_drones must be greater than 0 !")
        return max_drones