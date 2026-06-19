import re
from dataclasses import dataclass
from typing import Tuple
from base_parser import BaseParser
from colors import HubColor
from parser_errors import HubError


@dataclass
class HubConfig:
    loop: Tuple[int, int]
    color: HubColor
    max_drones: int = 1


class HubParser(BaseParser):

    def parse(self, line: str) -> HubConfig:
        tokens = self._split_line(line)
        self._key_validation(tokens[0])
        coordinates = self._coordinates_validation(tokens)
        attributes = self._parse_attributes(line)
        color = self._color_validation(attributes)
        max_drones = self._max_drones_validation(attributes)
        return HubConfig(loop=coordinates, color=color, max_drones=max_drones)

    def _split_line(self, line: str) -> list[str]:
        line = re.sub(r"\s*\[[^\]]+\]\s*$", "", line).strip()
        return line.split()

    def _key_validation(self, key: str) -> None:
        hub_key = key.lower().strip(": ")
        if hub_key != "hub":
            raise HubError("Invalid hub key !")
        
    def _coordinates_validation(self, tokens: list[str]) -> Tuple[int, int]:
        if len(tokens) < 4:
            raise HubError("Invalid hub format !")
        try:
            x = int(tokens[2])
            y = int(tokens[3])
            return x, y
        except ValueError:
            raise HubError("Invalid coordinates type !")
    
    def _color_validation(self, attributes: dict) -> HubColor:
        color_value = attributes.get("color")
        if not color_value:
            raise HubError("Missing color value !")
        try:
            return HubColor(color_value)
        except ValueError:
            raise HubError("Invalid color value !")
        
    def _max_drones_validation(self, attributes: dict) -> int:
        max_drones_str = attributes.get("max_drones", "1")
        try:
            max_drones = int(max_drones_str)
        except ValueError:
            raise HubError("Invalid max_drones value !")
        if max_drones <= 0:
            raise HubError("max_drones must be greater than 0 !")
        return max_drones