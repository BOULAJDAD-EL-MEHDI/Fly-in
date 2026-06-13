from parsers import BaseParser
from parsers import Tuple
from parsers import BaseModel, Field
from parsers import HubError
from parsers import HubColor


class Hub:
    pass

class HubConfig(BaseModel):
    loop: Tuple[int, int]
    color: str
    max_drones: int = Field(default=1, gt=0)


class HubParser(BaseParser, HubConfig):
    hub_key = "hub"

    def parse(self, line: str) -> HubConfig[Tuple[int, int], str, int]:
        hub_list = ()
        hub_list = self._split_line(line)
        self._key_validation(hub_list[0])
        coordinates = self._coordinates_validation(line)
        color = self._color_validation(line)
        max_drones = self._max_drones_validation(line)
        hub_list = coordinates, color, max_drones
        return hub_list


    def _split_line(self, line: str) -> Tuple[str, str]:
        hub_splited = ()
        hub_splited = line.split(" ")
        return hub_splited

    def _key_validation(self, key: str) -> None:
        hub_key = key.lower()
        hub_key = hub_key.strip(":")
        if hub_key != self.hub_key:
            raise HubError("Invalid hub key !")
        
    def _coordinates_validation(self, line: str) -> Tuple[int, int]:
        hub = ()
        if not (line[1].lower()).startswith("loop_"):
            raise HubError("Error in hub name !")
        try:
            x = int(line[2])
            y = int(line[3])
            hub = line[1],x, y
        except HubError:
            raise HubError("Invalide coordinates type !")
        return hub
    
    def _color_validation(self, line: str) -> str:
        color_key, color_value = line[4].split("=")
        color_key.strip("[")
        if color_key.lower() != "color":
            raise HubError("Invalid color key !")
        try:
            color_value = HubColor(color_value)
        except HubError:
            raise HubError("Invalid color key !")
        
    def _max_drones_validation(self, line: str) -> int:
        max_drones_key, max_drones_value = line[5].split("=")
        if max_drones_key.lower() != "max_drones":
            raise HubError("Invalid max_drones key !")
        max_drones_value = max_drones_value.strip("]")
        try:
            max_drones = int(max_drones_value)
        except HubError:
            raise HubError("Invalid max_drones Key !")
        return max_drones