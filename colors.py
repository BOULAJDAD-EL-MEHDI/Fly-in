from enum import Enum


class HubColor(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    ORANGE = "orange"
    PURPLE = "purple"
    PINK = "pink"
    BLACK = "black"
    WHITE = "white"
    GRAY = "gray"
    BROWN = "brown"
    CYAN = "cyan"
    MAGENTA = "magenta"
    LIME = "lime"
    NAVY = "navy"
    TEAL = "teal"
    OLIVE = "olive"
    MAROON = "maroon"
    SILVER = "silver"
    GOLD = "gold"
    DARKRED = "darkred"
    VIOLET = "violet"
    CRIMSON = "crimson"
    RAINBOW = "rainbow"

ANSI_COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
    "orange": "\033[38;5;208m",
    "purple": "\033[95m",
    "pink": "\033[38;5;213m",
    "black": "\033[30m",
    "white": "\033[97m",
    "gray": "\033[90m",
    "brown": "\033[38;5;94m",
    "cyan": "\033[96m",
    "magenta": "\033[35m",
    "lime": "\033[38;5;118m",
    "navy": "\033[38;5;18m",
    "teal": "\033[36m",
    "olive": "\033[38;5;100m",
    "maroon": "\033[38;5;52m",
    "silver": "\033[37m",
    "gold": "\033[38;5;220m",
    "darkred": "\033[38;5;88m",
    "violet": "\033[38;5;177m",
    "crimson": "\033[38;5;160m",
    "reset": "\033[0m",
}


def color_text(text, color):
    color = color.value if hasattr(color, "value") else color

    if color == "rainbow":
        colors = [
            "\033[91m",
            "\033[93m",
            "\033[92m",
            "\033[96m",
            "\033[94m",
            "\033[95m",
        ]
        return "".join(colors[i % 6] + c for i, c in enumerate(text)) + ANSI_COLORS["reset"]

    return f"{ANSI_COLORS.get(color, '')}{text}{ANSI_COLORS['reset']}"