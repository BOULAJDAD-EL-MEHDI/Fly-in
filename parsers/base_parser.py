from parsers import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse():
        pass