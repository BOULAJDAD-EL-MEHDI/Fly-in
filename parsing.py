class NbDrones(Exception):
    pass


class StartHub(Exception):
    pass


class EndHub(Exception):
    pass


class Hub(Exception):
    pass


class Connection(Exception):
    pass


def nb_drones_parsing(config_list: list) -> None:
    is_still  = 0
    nb_drones_count = 0
    for line in config_list:
        line.strip()
        if 

def g_parser() -> None:
    with open("config.txt") as config_text:
        config_text = config_text.readlines()
    nb_drones_parsing(config_text)

if __name__ == "__main__":
    g_parser()
  