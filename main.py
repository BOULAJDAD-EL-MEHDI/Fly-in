from parser_engine import ParserEngine


def main() -> None:
    config_path = "config.txt"
    config = ParserEngine(config_path).config
    print(type(config))    


if __name__ == "__main__":
    main()