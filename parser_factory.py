from nb_drones_parser import NbDronesParser
from start_hub_parser import StartHubParser
from end_hub_parser import EndHubParser
from hub_parser import HubParser
from connection_parser import ConnectionParser
from parser_errors import ParsingKeyError
from base_parser import BaseParser


class ParserFactory:
    """Create the correct parser implementation for a configuration key."""

    _parsers : dict[str, type[BaseParser]] = {
        "nb_drones": NbDronesParser,
        "start_hub": StartHubParser,
        "end_hub": EndHubParser,
        "hub": HubParser,
        "connection": ConnectionParser,
    }

    @classmethod
    def create(cls, key: str) -> BaseParser:
        """Return a parser instance matching the provided configuration key.

        Args:
            key: Configuration key such as "nb_drones" or "hub".

        Returns:
            An initialized parser instance.

        Raises:
            ParsingKeyError: If the key does not map to a registered parser.
        """
        try:
            parser_class = cls._parsers[key]
        except KeyError:
            raise ParsingKeyError(f"Invalid key: {key}")

        return parser_class()
