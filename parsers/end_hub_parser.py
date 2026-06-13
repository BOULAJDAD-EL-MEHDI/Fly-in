from parsers import BaseParser
from parsers import Tuple
from parsers import BaseModel, Field
from parsers import EndHubError
from parsers import HubColor


class Hub:
    pass

class EndHubConfig(BaseModel):
    end_hub: Tuple[int, int]
    color: str
    max_drones: int = Field(default=1, gt=0)


class EndHubParser(BaseParser, EndHubConfig):
    end_key = "end_hudb"

    def parse(self, line: str) -> EndHubConfig[Tuple[int, int], str, int]:
        end_hub_list = ()
        end_hub_list = self._split_line(line)
        self._key_validation(end_hub_list[0])
        coordinates = self._coordinates_validation(line)
        color = self._color_validation(line)
        max_drones = self._max_drones_validation(line)
        end_hub_list = coordinates, color, max_drones
        return end_hub_list


    def _split_line(self, line: str) -> Tuple[str, str]:
        start_hub_splited = ()
        start_hub_splited = line.split(" ")
        return start_hub_splited

    def _key_validation(self, key: str) -> None:
        end_key = key.lower()
        key = key.strip()
        if end_key != self.end_key:
            raise EndHubError("Invalid end_hub key !")
        
    def _coordinates_validation(self, line: str) -> Tuple[int, int]:
        end_hub = ()
        if line[1].lower() != "goal":
            raise EndHubError("the goal name of coordinates dos not exist !")
        try:
            x = int(line[2])
            y = int(line[3])
            end_hub = x, y
        except Exception:
            raise EndHubError("Invalide coordinates type !")
        return end_hub
    
    def _color_validation(self, line: str) -> str:
        color_key, color_value = line[4].split("=")
        color_key.strip("[")
        if color_key.lower() != "color":
            raise EndHubError("Invalid color key !")
        try:
            color_value = HubColor(color_value)
        except EndHubError:
            raise EndHubError("Invalid color key !")
        
    def _max_drones_validation(self, line: str) -> int:
        max_drones_key, max_drones_value = line.split("=")
        if max_drones_key.lower() != "max_drones":
            raise EndHubError("Invalid max_drones key !")
        max_drones_value = max_drones_value.strip("]")
        try:
            max_drones = int(max_drones_value)
        except EndHubError:
            raise EndHubError("Invalid max_drones Key !")
        return max_drones