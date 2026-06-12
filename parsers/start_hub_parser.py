from parsers import BaseParser
from parsers import Dict, Tuple
from parsers import BaseModel, Field
from parsers import StartHubError
from parsers import HubColor


class Hub:
    pass

class StartHubConfig(BaseModel):
    start_hub: Tuple[int, int]
    color: str
    max_drones: int(default=1, gt=0)


class StartHubParser(BaseParser, StartHubConfig):
    start_key = "start_hudb"

    def parse(self, line: str) -> StartHubConfig[Tuple[int, int], str, int]:
        start_hub_list = ()
        start_hub_list = self._split_line(line)
        self._key_validation(start_hub_list[0])
        coordinates = self._coordinates_validation(line)
        color = self._color_validation(line)
        max_drones = self._max_drones_validation(line)
        start_hub_list = coordinates, color, max_drones

        


    def _split_line(self, line: str) -> Tuple[str, str]:
        start_hub_splited = ()
        start_hub_splited = line.split(" ")
        return start_hub_splited

    def _key_validation(self, key: str) -> None:
        start_key = key.lower()
        key = key.strip()
        if start_key != self.start_key:
            raise StartHubError("Invalid start_hub key !")
        
    def _coordinates_validation(self, line: str) -> Tuple[int, int]:
        start_hub = ()
        if line[1].lower() != "start":
            raise StartHubError("the start name of coordinates dos not exist !")
        try:
            x = int(line[2])
            y = int(line[3])
            start_hub = x, y
        except Exception:
            raise StartHubError("Invalide coordinates type !")
        return start_hub
    
    def _color_validation(self, line: str) -> str:
        color_key, color_value = line[4].split("=")
        color_key.strip("[")
        if color_key.lower() != "color":
            raise StartHubError("Invalid color key !")
        try:
            color_value = HubColor(color_value)
        except StartHubError:
            raise StartHubError("Invalid color key !")
        
    def _max_drones_validation(self, line: str) -> int:
        max_drones_key, max_drones_value = line.split("=")
        if max_drones_key.lower() != "max_drones":
            raise StartHubError("Invalid max_drones key !")
        max_drones_value = max_drones_value.strip("]")
        try:
            max_drones = int(max_drones_value)
        except StartHubError:
            raise StartHubError("Invalid max_drones Key !")
        return max_drones