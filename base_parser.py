from parsers import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def parse(self, line: str) -> object:
        """Parse a config line and return a config object."""
        pass