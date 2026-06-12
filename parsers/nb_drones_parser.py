from parsers import BaseParser
from parsers import Dict, Tuple
from parsers import BaseModel, Field
from parsers import NbDronesError


class NbDronesConfig(BaseModel):
    nb_drones: int = Field(gt=0)


class NbDronesParser(BaseParser):
    nb_drones_key = "nb_drones"

    def parse(self, line: str) -> Tuple[str, int]:
        self._split_line(line)
        nb_drones_key, value = self._parse_value(value)
        nb_drones_key = self._parse_key(nb_drones_key)
        value = self._parse_value(value)
        return nb_drones_key, value

    def _split_line(self, line: str) -> Tuple[str, str]:
        nb_drones_key, value = line.split(":")
        nb_drones_key = nb_drones_key.strip()
        value = value.strip()
        return nb_drones_key, value

    def _parse_value(self, value: str) -> int:
        try:
             value = int(value)
        except NbDronesError:
            raise NbDronesError("nb_derones must be integer")
        
        try:
            nb_drones = value
        except NbDronesError:
            raise NbDronesError("nb_drones must be grater than 0 !")
        return nb_drones
    
    def _parse_key(self, key: str) -> str:
        if self.nb_drones_key != key.lower():
            raise NbDronesError("Invalid Key !")
        return key
