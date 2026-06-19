from nb_drones_parser import NbDronesParser
from start_hub_parser import StartHubParser
from end_hub_parser import EndHubParser
from hub_parser import HubParser
from connection_parser import ConnectionParser
from parser_errors import ParsingKeyError
from base_parser import BaseParser


class ParserFactory:

    _parsers = {
        "nb_drones": NbDronesParser,
        "start_hub": StartHubParser,
        "end_hub": EndHubParser,
        "hub": HubParser,
        "connection": ConnectionParser,
    }

    @classmethod
    def create(cls, key: str) -> BaseParser:
        try:
            return cls._parsers[key]()
        except KeyError:
            raise ParsingKeyError(f"Invalid key: {key}")
