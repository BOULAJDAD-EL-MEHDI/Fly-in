from parser_engine import ParserEngine


def main() -> None:
    config_path = "config.txt"
    for item in ParserEngine(config_path).config:
        print(item)


if __name__ == "__main__":
    main()