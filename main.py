from parser_engine import ParserEngine
import sys

def main(config: str) -> None:
    config = ParserEngine(config).config
    for line in config:
        print(line)


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 2:
        print("invalide arg input !")
        sys.exit(1)
    else:
        try:
            main(sys.argv[1])
        except Exception as e:
            print(f"Error {e}")
            sys.exit(1)