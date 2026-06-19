from parser_factory import ParserFactory

class ParserEngine:

    def __init__(self, config_path: str) -> None:
        self.config = self.parse_file(config_path)

    def parse_file(self, file_path: str) -> list:
        config = []

        with open(file_path) as file:
            for line in file:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue

                key = line.split(":", 1)[0].lower()
                parser = ParserFactory.create(key)
                obj = parser.parse(line)
                config.append(obj)

        return config