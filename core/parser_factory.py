from core import nb_drones_parser
from core import start_hub_parser
from core import end_hub_parser
from core import hub_parser
from core import connection_parser
from core import List
from core import ConfigError


class FactoryParser:
    with open("config.txt") as config_text:
        config_lines = config_text.readlines()
    
    def _key_verify(self, config_lines: List) -> None:
        errors = []

        validators = [
            self._nb_drones_key_verify,
            self._start_hub_key_verify, 
            self._end_hub_key_verify,
            self._hub_key_verify,
            self._connection_key_verify,
        ]

        for validator in validators:
            try:
                validator(config_lines)
            except Exception as e:
                errors.append(str(e))

        if errors:
            raise ConfigError("\n".join(errors))
        
    def _nb_drones_key_verify(self, lines: List) -> None:
        




    def _kyes_geter(self, lines: str) -> None:
        keys = []

        for line in lines:
            line = line.strip()
            if not line.startswith("#"):
                line = line.split(":")
                line.lower()
                keys.append(line)

    def _start_hub_verify(self, lines: str) -> None:
        pass

    def _end_hub_verify(self, lines: str) -> None:
        pass

    def _hub_key_verify(self, lines: str) -> None:
        pass

    def _connections_verify(self, lines: str) -> None:
        pass
