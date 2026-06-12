from parsers import BaseParser
from parsers import Dict, Tuple
from parsers import BaseModel, Field
from parsers import StartHubError


class Hub:
    pass

class StartHubConfig(BaseModel):
    start_hub: Tuple[int, int]
    color: str
    max_drones: int


class StartHubParser(BaseParser):
    start_key = "start_hudb"

    def parse(self, line: str) -> StartHubConfig:
        start_hub_list = ()
        start_hub_list = self._split_line(line)
        self._key_validation(start_hub_list[0])
        coordinates = self._coordinates_validation(line)
        color = self._color_validation(line)
        


    def _split_line(self, line: str) -> Tuple[str, str]:
        start_hub_splited = ()
        start_hub_splited = line.split(" ")
        return start_hub_splited

    def _key_validation(self, key: str) -> None:
        start_key = key.lower()
        key = key.strip()
        if start_key.lower() != self.start_key:
            raise StartHubError("Invalid key !")
        
    def _coordinates_validation(self, line: Tuple) -> Tuple[int, int]:
        coordinates = ()
        try:
            x = int(line[2])
            y = int(line[3])
        except Exception:
            raise StartHubError("Invalide coordinates !")
        return coordinates(x, y)
    
    def _color_validation(self, line: Tuple) -> str:
        color_config = line[4].split("=")
        color = ""
        if 


    
        