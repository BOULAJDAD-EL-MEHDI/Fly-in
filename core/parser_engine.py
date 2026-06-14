from core import ParserFactory


class ParserEngine:

    def parse_file(self, file_path: str):

        with open(file_path) as file:

            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key = line.split(":")[0]
                key = key.lower()

                parser = ParserFactory.create(key)

                obj = parser.parse(line)