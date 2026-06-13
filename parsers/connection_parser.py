from parsers import BaseParser
from parsers import Tuple
from parsers import List
from parsers import ConnectionsError
from parsers import BaseModel
from parsers import Field


class ConnectionConfig(BaseModel):
    connection: Tuple[int, int]
    color:str
    max_link_capacity: int = Field()

class ConnectionParser(BaseParser, ConnectionConfig):
    connection_key = "connection"

    def parse(sefl, line: str) -> ConnectionConfig[Tuple[int, int], str, int]:
        hub_list = []
        hub_list = self._split_line(line)
        self._key_validation(hub_list[0])
        coordinates = self._connections_validation(line[1])
        color = self._color_validation(line)
        max_drones = self._max_drones_validation(line)
        end_hub_list = coordinates, color, max_drones
        return end_hub_list
    
    def _split_line(self, line: str) -> List:
        start_hub_splited = []
        start_hub_splited = line.split(" ")
        return start_hub_splited
    
    def _key_validation(self, key: str) -> None:
        connection_key = key.lower()
        connection_key = connection_key.strip(":")
        if connection_key != self.connection_key:
            raise ConnectionsError("Invalid connection key !")
        
    def _connections_validation(self, line: str) -> Tuple[str, str]:
        loops = ()
        first_loop, second_loop = line.split("-")
        first_loop, second_loop = first_loop.lower(), second_loop.lower()
        if not first_loop.startswith("loop_"):
            raise ConnectionsError("Problem in first loop !")
        if not second_loop.startswith("loop_"):
            raise ConnectionsError("Problem in second loop !")
        loops = first_loop, second_loop
        return loops

    def _link_capacity(self, line: str) -> int:
        link_capacity = link_capacity.strip("[]")
        link_capacity_key, link_capacity_value = link_capacity.split("=")
        link_capacity_key = link_capacity_key.lower()
        if link_capacity_key != "max_link_capacity":
            raise ConnectionsError("Invalid link capacity key !")
        try:
            self.max_link_capacity = int(link_capacity)
        except Exception:
            raise ConnectionError("Invalid link capacity value !")
        
