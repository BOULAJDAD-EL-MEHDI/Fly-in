from parsers import BaseParser
from parsers import List
from parsers import BaseModel, Field
from parsers import NbDronesError
from parsers import ValidationError-


class NbDronesConfig(BaseModel):
    nb_drones: int = Field(gt=0)


class NbDronesParser(BaseParser):

    def parse(self, line: str) -> NbDronesConfig:
        line = self._split_line(line)
        self._parse_key(line[0])
        nb_drones_value = self._parse_value(line[1])
        try:
            return NbDronesConfig(nb_drones=nb_drones_value)
        except ValidationError:
            raise NbDronesError("nb_drones must be greater than 0!")

    def _split_line(self, line: str) -> List[str]:
        return line.split(":")

    
    def _parse_key(self, key: str) -> None:
        if key.strip().lower() != "nb_drones":
            raise NbDronesError("Invalid nb_drones Key !")
        
    def _parse_value(self, value: str) -> int:
        try:
            return int(value.strip())
        except ValueError:
            raise NbDronesError("nb_drones must be integer!")