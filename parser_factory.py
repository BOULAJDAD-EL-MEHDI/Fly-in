from core import NbDronesParser
from core import StartHubParser
from core import EndHubParser
from core import HubParser
from core import ConnectionParser
from core import ParsingKeyError
from core import BaseParser


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
