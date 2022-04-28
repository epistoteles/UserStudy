import re


# ansi escape codes
colors = {
    "purple": 95,
    "cyan": 96,
    "darkcyan": 36,
    "blue": 94,
    "green": 92,
    "yellow": 93,
    "red": 91,
}


def remove_formatting(text):
    return re.sub(r"\x1B\[\d+m", "", text)


def ansi_escape(text, i):
    texts = text.split("\n")
    result = [f"\x1B[{i}m{x}\x1B[0m" for x in texts]
    return "\n".join(result)


def bold(text):
    return ansi_escape(text, 1)


def grey(text):
    return ansi_escape(text, 2)


def gray(text):
    return grey(text)


def italic(text):
    return ansi_escape(text, 3)


def underline(text):
    return ansi_escape(text, 4)


def blink(text):
    return ansi_escape(text, 5)


def blocked(text):
    return ansi_escape(text, 7)


def striked(text):
    return ansi_escape(text, 9)


def color(text, c="red"):
    texts = text.split("\n")
    result = [ansi_escape(line, colors[c]) for line in texts]
    return "\n".join(result)
