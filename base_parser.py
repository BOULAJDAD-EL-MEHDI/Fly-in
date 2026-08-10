from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base class for parsing configuration lines."""

    @abstractmethod
    def parse(self, line: str) -> object:
        """Parse a configuration line into a config object.

        Args:
            line: Raw configuration line to parse.

        Returns:
            A parsed configuration object.
        """
        pass

    def _parse_attributes(self, line: str) -> dict:
        """Extract metadata attributes enclosed in square brackets.

        Args:
            line: Raw configuration line that may contain metadata.

        Returns:
            A dictionary of parsed attribute names and values.

        Raises:
            ValueError: If the metadata block is malformed.
        """
        stripped_line = line.strip()
        open_count = stripped_line.count("[")
        close_count = stripped_line.count("]")

        if open_count == 0 and close_count == 0:
            return {}
        if open_count != 1 or close_count != 1:
            raise ValueError("Invalid metadata block syntax !")

        opening_bracket = stripped_line.find("[")
        closing_bracket = stripped_line.rfind("]")
        if opening_bracket == -1 or closing_bracket == -1 or closing_bracket < opening_bracket:
            raise ValueError("Invalid metadata block syntax !")

        if stripped_line[closing_bracket + 1 :].strip():
            raise ValueError("Invalid metadata block syntax !")

        attributes_raw = stripped_line[opening_bracket + 1 : closing_bracket].strip()
        if not attributes_raw:
            raise ValueError("Empty metadata block !")

        attributes = {}
        for token in attributes_raw.split():
            if "=" not in token:
                raise ValueError("Malformed metadata pair without = !")
            key, value = token.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if not key or not value:
                raise ValueError("Malformed metadata pair with empty key or value !")
            if key in attributes:
                raise ValueError("Duplicate metadata key in block !")
            attributes[key] = value
        return attributes