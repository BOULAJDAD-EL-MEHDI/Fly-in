from parsers import BaseParser
from parsers import Dict, Tuple
from parsers import BaseModel, Field
from parsers import StartHubError


class Hub

class StartHubConfig(BaseModel):
    start_hub: Tuple[int, int]
    color: str
    max_drones: int


class StartHubParser(BaseParser):
    start_key = "start__hub"

    def parse(self, line: str) -> StartHubConfig:
        splitd = self._split_line(line)
        self._key_validation(line)
        coordinates = self._coordinates_validation(line)
        color = self._color_validation(line)
        


    def _split_line(self, line: str) -> Tuple[str, str]:
        start_hub_splited = ()
        start_hub_splited = line.split(" ")
        return start_hub_splited

    def _key_validation(self, line: Tuple) -> None:
        start_key = line[0].lower()
        if start_key != self.start_key:
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


    
        