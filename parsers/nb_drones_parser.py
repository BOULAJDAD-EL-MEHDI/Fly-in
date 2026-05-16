from parsers import BaseParser
from parsers import Dict, Tuple, List
from ..exeptions import NbDronesError

class NbDronesParser(BaseParser):
    def __init__(self, config: str) -> None:
        self.config = config

    def parse(config: List) ->  Dict[str, Tuple]:
        config_len = len(config)
        config[0] = config[0].lower()
        if not config[0].startswith("nb_drones"):
            raise NbDronesError('the config file is not starting with "nb_drones" parameter !')
        for i in range(1, config_len):
            config[i] = config[i].lower()
            if config[i].startswith("nb_drones"):
                raise NbDronesError('to many "nb_drones" parameters!')
        key, value = config[0].split(":")
        nb_drones_config: Dict[str, Tuple[str, str]] = {
            key.strip(): (key.strip(), value.strip())
        }

        return nb_drones_config
    

        
