from dataclasses import dataclass
from typing import Tuple
from base_parser import BaseParser
from parser_errors import ConnectionsError


@dataclass
class ConnectionConfig:
    connection: Tuple[str, str]
    link_capacity: int = 1


class ConnectionParser(BaseParser):

    def parse(self, line: str) -> ConnectionConfig:
        fields = self._split_line(line)
        if len(fields) < 2:
            raise ConnectionsError("Connection line is empty !")
        if len(fields) != 2:
            raise ConnectionsError("Invalid connection format !")
        self._key_validation(fields[0])
        connection = self._connections_validation(fields[1])
        attributes = self._parse_attributes(line)
        self._validate_attributes(attributes)
        max_link_capacity = self._link_capacity(attributes)
        return ConnectionConfig(connection=connection, link_capacity=max_link_capacity)

    def _split_line(self, line: str) -> list[str]:
        line = line.strip()
        if line.endswith("]"):
            pos = line.rfind("[")
            if pos != -1:
                line = line[:pos].rstrip()
        return line.split()

    def _key_validation(self, key: str) -> None:
        connection_key = key.lower().strip(": ")
        if connection_key != "connection":
            raise ConnectionsError("Invalid connection key !")
        
    def _connections_validation(self, line: str) -> Tuple[str, str]:
        connections = line.split("-")
        if len(connections) != 2:
            raise ConnectionsError("Invalid connections: must contain two hubs !")

        first, second = connections[0].strip(), connections[1].strip()
        if not first:
            raise ConnectionsError("Connection missing first endpoint !")
        if not second:
            raise ConnectionsError("Connection missing second endpoint !")
        if first == second:
            raise ConnectionsError("Self-loop connection !")
        invalid_chars = set(" []=")
        if any(char in first for char in invalid_chars) or any(char in second for char in invalid_chars):
            raise ConnectionsError("Invalid connection endpoint !")
        return first, second

    def _validate_attributes(self, attributes: dict) -> None:
        allowed_keys = {"max_link_capacity"}
        for key in attributes:
            if key not in allowed_keys:
                raise ConnectionsError("Unknown metadata key !")

    def _link_capacity(self, attributes: dict) -> int:
        raw_value = attributes.get("max_link_capacity", "1")
        try:
            max_link_capacity = int(raw_value)
        except ValueError:
            raise ConnectionsError("Invalid link capacity value !")
        if max_link_capacity <= 0:
            raise ConnectionsError("max_link_capacity must be greater than 0 !")
        return max_link_capacity
        
