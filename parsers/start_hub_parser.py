from parsers import BaseParser
from parsers import List, Tuple
from parsers import BaseModel, Field
from parsers import StartHubError
from parsers import HubColor


class StartHubConfig(BaseModel):
    start_hub: Tuple[int, int]
    color: HubColor
    max_drones: int = Field(default=1, gt=0)


class StartHubParser(BaseParser):

    def parse(self, line: str) -> StartHubConfig:
        start_hub_list = []
        start_hub_list = self._split_line(line)
        self._key_validation(start_hub_list[0])
        coordinates = self._coordinates_validation(start_hub_list)
        if len(start_hub_list) == 5:
            color = self._color_validation(start_hub_list[4])
            return StartHubConfig(start_hub = coordinates, color = color, max_drones = 1)
        elif len(start_hub_list) == 6:
            color = self._color_validation(start_hub_list[4])
            max_drones = self._max_drones_validation(start_hub_list[5])
            return StartHubConfig(start_hub = coordinates, color = color, max_drones = max_drones)
        else:
            raise StartHubError("Invalide start_hub format !")

    def _split_line(self, line: str) -> List[str]:
        start_hub_splited = []
        start_hub_splited = line.split(" ")
        return start_hub_splited

    def _key_validation(self, key: str) -> None:
        start_key = key.lower().strip(":")
        if start_key != "start_hub":
            raise StartHubError("Invalid start_hub key !")
        
    def _coordinates_validation(self, line: List) -> Tuple[int, int]:
        start_hub = ()
        if line[1].lower().strip() != "start":
            raise StartHubError("the start name of coordinates dos not exist !")
        try:
            x = int(line[2])
            y = int(line[3])
            start_hub = x, y
        except ValueError:
            raise StartHubError("Invalide coordinates type !")
        return start_hub
    
    def _color_validation(self, line: str) -> str:
        color_key, color_value = line.split("=")
        color_key = color_key.strip("[ ]")
        if color_key.lower() != "color":
            raise StartHubError("Invalid color key !")
        try:
            color_value = HubColor(color_value)
            return color_value
        except Exception:
            raise StartHubError("Invalid color value !")
        
    def _max_drones_validation(self, line: str) -> int:
        max_drones_key, max_drones_value = line.split("=")
        if max_drones_key.lower() != "max_drones":
            raise StartHubError("Invalid max_drones key !")
        max_drones_value = max_drones_value.strip("]")
        try:
            max_drones = int(max_drones_value)
        except Exception:
            raise StartHubError("Invalid max_drones Key !")
        return max_drones