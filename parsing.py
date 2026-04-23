def manual_parser():
    f = open("config.txt", "r")
    text = f.readlines
    return text


def parser():
    try:
        txt = manual_parser()
        return txt
    except Exception as e:
        print(e)


if __name__ == "__main__":
    text = parser()
    print(text)