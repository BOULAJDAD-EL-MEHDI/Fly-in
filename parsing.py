def param_chaker(config: list, param: str) -> bool:
    s_lines = []
    param_count = 0
    for line in config:
        s_lines.append(line.lstrip())
    for line in s_lines:
        if line.startswith(param):
            param_count += 1
    if param_count != 1:
        raise f"config file contain {nb_drones} lines that defind nb_drones !"
        return 0
    else:
        return 1
        

 

def manual_parser():
    f = open("config.txt", "r")
    text = f.readlines()
    try:
        if(param_chaker(text, "nb_drones") or param_chaker(text, "start_hub") or param_chaker(text, "end_hub")):
            print("all good !")
    except Exception as e:
        print(f"Error {e}")


def parser():
    try:
        txt = manual_parser()
        return txt
    except Exception as e:
        print(e)


if __name__ == "__main__":
    text = parser()
    print(text)