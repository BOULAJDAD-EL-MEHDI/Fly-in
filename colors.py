from enum import Enum


class HubColor(Enum):
    """Supported display colors for hubs in the simulation output."""

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
    """Apply ANSI color formatting to text.

    Args:
        text: Text to display.
        color: Color name or HubColor enum value to apply.

    Returns:
        The formatted text with ANSI color codes.
    """
    color = color.value if hasattr(color, "value") else color

    return f"{ANSI_COLORS.get(color, '')}{text}{ANSI_COLORS['reset']}"