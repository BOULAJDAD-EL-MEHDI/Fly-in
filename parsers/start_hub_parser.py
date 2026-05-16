from parsers import BaseParser
from parsers import Dict, Tuple

class StartHubParser(BaseParser):
    def __init__(self, config: str) -> None:
        self.config = config
        self.start_hub_data = {}

    def parse(config: str) ->  Dict[str, Tuple]:
        is_first = 1