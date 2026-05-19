from parsers import BaseParser
from parsers import Dict, Tuple
from parsers import BaseModel, Field
from parsers import NbDronesError


class NbDronesConfig(BaseModel):
    nb_drones: int = Field(gt=0)


class NbDronesParser(BaseParser):
    nb_drones_key = "nb_drones"

    def parse(self, line: str) -> NbDronesConfig:
        nb_drones_key, value = self._split_line(line)
        self._validate_nb_drones_key(nb_drones_key)
        value = self._parse_value(value)
        return NbDronesConfig(nb_drones = value)
    
    def _split_line(self, line: str) -> Tuple[str, str]:
        self.nb_drones_key, Value = line.split(":")
        if nb_drones_key.lower() != self.nb_drones_key:
            raise NbDronesError("Invalid_nb_drones_key")


    def parse_value(self, value: str) -> int:
        try:
             return int(value)
        except NbDronesError:
            raise NbDronesError("nb_derones must be integer") 
