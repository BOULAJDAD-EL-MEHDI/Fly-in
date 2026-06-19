import re
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
        self._key_validation(fields[0])
        connection = self._connections_validation(fields[1])
        attributes = self._parse_attributes(line)
        max_link_capacity = self._link_capacity(attributes)
        return ConnectionConfig(connection=connection, link_capacity=max_link_capacity)

    def _split_line(self, line: str) -> list[str]:
        line = re.sub(r"\s*\[[^\]]+\]\s*$", "", line).strip()
        return line.split()

    def _key_validation(self, key: str) -> None:
        connection_key = key.lower().strip(": ")
        if connection_key != "connection":
            raise ConnectionsError("Invalid connection key !")
        
    def _connections_validation(self, line: str) -> Tuple[str, str]:
        connections = line.split("-")
        if len(connections) != 2:
            raise ConnectionsError("Invalid connections: must contain two hubs !")
        return connections[0], connections[1]

    def _link_capacity(self, attributes: dict) -> int:
        raw_value = attributes.get("max_link_capacity", "1")
        try:
            return int(raw_value)
        except ValueError:
            raise ConnectionsError("Invalid link capacity value !")
        
