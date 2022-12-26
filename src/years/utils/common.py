
def strip_line(line: str) -> str:
    stripped_line = line.strip()
    return '' if len(stripped_line) == 0 else stripped_line


def strip_lines(lines: list[str]) -> list[str]:
    return list(map(strip_line, lines))


def remove_newline(line: str) -> str:
    return line.replace('\n', '')


def remove_newlines(lines: list[str]) -> list[str]:
    return list(map(remove_newline, lines))
