from parsers import BaseParser
from parsers import Dict, Tuple
from parsers import BaseModel, Field
from parsers import NbDronesError


class NbDronesConfig(BaseModel):
    nb_drones: int = Field(gt=0)


class NbDronesParser(BaseParser):
    nb_drones_key = "nb_drones"

    def parse(self, line: str) -> NbDronesConfig:
        try:
            self._split_line(line)
            value = self._parse_value(value)
            return NbDronesConfig(nb_drones = value)
        except NbDronesError:
            raise NbDronesError("Invalide nb_drones key !")

    def _split_line(self, line: str) -> Tuple[str, str]:
        nb_drones_key, value = line.split(":")
        nb_drones_key = nb_drones_key.strip()
        value = value.strip()
        if nb_drones_key.lower() != self.nb_drones_key:
            raise NbDronesError("Invalid nb_drones_key !")
        return nb_drones_key, value

    def _parse_value(self, value: str) -> int:
        try:
             value = int(value)
             nb_drones = value
             return nb_drones
        except NbDronesError:
            raise NbDronesError("nb_derones must be integer")
