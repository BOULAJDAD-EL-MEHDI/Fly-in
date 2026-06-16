from parsers import BaseParser
from parsers import Tuple
from parsers import List
from parsers import ConnectionsError
from parsers import BaseModel


class ConnectionConfig(BaseModel):
    connection: Tuple
    link_capacity: int

class ConnectionParser(BaseParser):

    def parse(self, line: str) -> ConnectionConfig:
        connection_list = self._split_line(line)
        self._key_validation(connection_list[0])
        connection = self._connections_validation(connection_list[1])
        if len(connection_list) == 3:
            max_link_capacity = self._link_capacity(connection_list[2])
            return ConnectionConfig(connection = connection, max_link_capacity = max_link_capacity)
        return ConnectionConfig(connection = connection, max_link_capacity = 1)
    
    def _split_line(self, line: str) -> List:
        return line.split(" ")
    
    def _key_validation(self, key: str) -> None:
        connection_key = key.lower().strip(": ")
        if connection_key != "connection":
            raise ConnectionsError("Invalid connection key !")
        
    def _connections_validation(self, line: str) -> Tuple[str, str]:
        connections = line.split("-")
        if len(connections) != 2:
            raise ConnectionError("Invalide connections: must contain two hubs !")
        return connections[0],connections[1]

    def _link_capacity(self, line: str) -> int:
        link_capacity = line.strip("[]")
        link_capacity_key, max_link_capacity = link_capacity.split("=")
        if link_capacity_key.lower() != "max_link_capacity":
            raise ConnectionsError("Invalid link capacity key !")
        try:
            return int(max_link_capacity)
        except ValueError:
            raise ConnectionError("Invalid link capacity value !")
        
