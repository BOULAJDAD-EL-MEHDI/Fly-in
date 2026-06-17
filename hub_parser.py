from parsers import BaseParser
from parsers import Tuple
from parsers import BaseModel, Field
from parsers import HubError
from parsers import HubColor


class HubConfig(BaseModel):
    loop: Tuple[int, int]
    color: HubColor
    max_drones: int = Field(default=1, gt=0)


class HubParser(BaseParser):

    def parse(self, line: str) -> HubConfig:
        hub_list = self._split_line(line)
        self._key_validation(hub_list[0])
        coordinates = self._coordinates_validation(line)

        if len(hub_list) == 5:
            color = self._color_validation(hub_list[4])
            return HubConfig(hub = coordinates, color = color)
        
        elif len(hub_list) == 6:
            color = self._color_validation(hub_list[4])
            max_drones = self._max_drones_validation(hub_list[5])
            return HubConfig(hub = coordinates, color = color, max_drones = max_drones)
        
        else:
            raise HubError("Invalid Hub format !")

    def _split_line(self, line: str) -> Tuple[str, str]:
        hub_splited = ()
        hub_splited = line.split(" ")
        return hub_splited

    def _key_validation(self, key: str) -> None:
        hub_key = key.lower().strip(": ")
        if hub_key != "hub":
            raise HubError("Invalid hub key !")
        
    def _coordinates_validation(self, line: str) -> Tuple[str, int, int]:
        hub = ()
        try:
            x = int(line[2])
            y = int(line[3])
            hub = line[1],x, y
        except HubError:
            raise HubError("Invalide coordinates type !")
        return hub
    
    def _color_validation(self, line: str) -> str:
        color_key, color_value = line.split("=")
        color_key.strip("[ ")
        if color_key.lower() != "color":
            raise HubError("Invalid color key !")
        try:
            color_value = HubColor(color_value)
        except Exception:
            raise HubError("Invalid color key !")
        
    def _max_drones_validation(self, line: str) -> int:
        max_drones_key, max_drones_value = line.split("=")
        if max_drones_key.lower() != "max_drones":
            raise HubError("Invalid max_drones key !")
        max_drones_value = max_drones_value.strip("] ")
        try:
            max_drones = int(max_drones_value)
        except ValueError:
            raise HubError("Invalid max_drones Key !")
        return max_drones