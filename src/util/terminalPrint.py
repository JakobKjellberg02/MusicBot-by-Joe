from enum import Enum
class TColor(Enum):

    OK = '\033[32m'
    ERR = '\033[31m'
    RESET = '\033[0m'

    @staticmethod
    def colorize(text, *colors: "TColor"):
        color_codes = ''.join([color.value for color in colors])
        return f"{color_codes}{text}{TColor.RESET.value}"

