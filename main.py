from parser_engine import ParserEngine


def main(config_path: str = "config.txt") -> int:
    engine = ParserEngine(config_path)
    for item in engine.config:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())