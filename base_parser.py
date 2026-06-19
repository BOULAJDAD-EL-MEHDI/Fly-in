import re
from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def parse(self, line: str) -> object:
        """Parse a config line and return a config object."""
        pass

    def _parse_attributes(self, line: str) -> dict:
        match = re.search(r"\[([^\]]+)\]\s*$", line.strip())
        if not match:
            return {}

        attributes = {}
        for token in match.group(1).split():
            if "=" in token:
                key, value = token.split("=", 1)
                attributes[key.strip().lower()] = value.strip()
        return attributes