from dataclasses import dataclass
from typing import Tuple
from base_parser import BaseParser
from colors import HubColor
from parser_errors import EndHubError
from typing import Optional


@dataclass
class EndHubConfig:
    name: str
    end_hub: Tuple[int, int]
    color: HubColor | None
    zone: str | None = None
    max_drones: int = 1


class EndHubParser(BaseParser):

    def parse(self, line: str) -> EndHubConfig:
        tokens = self._split_line(line)
        self._key_validation(tokens[0])
        coordinates = self._coordinates_validation(tokens)
        attributes = self._parse_attributes(line)
        self._validate_attributes(attributes)
        color = self._color_validation(attributes)
        max_drones = self._max_drones_validation(attributes)
        zone = self._zone_validation(attributes)
        return EndHubConfig(name=tokens[1], end_hub=coordinates, color=color,zone=zone, max_drones=max_drones)

    def _split_line(self, line: str) -> list[str]:
        line = line.strip()
        if line.endswith("]"):
            pos = line.rfind("[")
            if pos != -1:
                line = line[:pos].rstrip()
        return line.split()

    def _key_validation(self, key: str) -> None:
        end_key = key.lower().strip(" :")
        if end_key != "end_hub":
            raise EndHubError("Invalid end_hub key !")
        
    def _coordinates_validation(self, tokens: list[str]) -> Tuple[int, int]:
        if len(tokens) < 4:
            raise EndHubError("Invalid end_hub format !")
        name = tokens[1]
        if any(char in name for char in "- []="):
            raise EndHubError("Invalid zone name !")
        try:
            x = int(tokens[2])
            y = int(tokens[3])
            return x, y
        except ValueError:
            raise EndHubError("Invalid coordinates type !")
    
    def _validate_attributes(self, attributes: dict) -> None:
        allowed_keys = {"color", "max_drones", "zone"}
        for key in attributes:
            if key not in allowed_keys:
                raise EndHubError("Unknown metadata key !")

    def _color_validation(self, attributes: dict) -> Optional[HubColor]:
        color_value = attributes.get("color")
        if not color_value:
            return None
        try:
            return HubColor(color_value)
        except ValueError:
            raise EndHubError("Invalid color value !")
        
    def _max_drones_validation(self, attributes: dict) -> int:
        max_drones_str = attributes.get("max_drones", "1")
        try:
            max_drones = int(max_drones_str)
        except ValueError:
            raise EndHubError("Invalid max_drones value !")
        if max_drones <= 0:
            raise EndHubError("max_drones must be greater than 0 !")
        return max_drones
    
    def _zone_validation(self, attributes: dict) -> str | None:
        zone_value = attributes.get("zone")
        if zone_value is None:
            return None
        if not zone_value:
            raise EndHubError("Zone type is empty !")
        valid_zones = {"normal", "restricted", "priority", "blocked"}
        if zone_value not in valid_zones:
            raise EndHubError("Invalid zone type !")
        return zone_value
