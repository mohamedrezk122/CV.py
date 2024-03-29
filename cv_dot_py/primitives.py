from termcolor import cprint


def put_warning(msg: str):
    cprint("WARNING: ", "yellow", end="")
    print(msg)


def put_error(msg: str):
    cprint("ERROR: ", "red", end="")
    print(msg)


def put_success(msg: str):
    cprint("SUCCESS: ", "green", end="")
    print(msg)


def batch_replace(string: str, replacements: dict) -> str:
    if not string.strip():
        return string
    for replacement in replacements:
        string = string.replace(replacement, str(replacements[replacement]))
    return string


def latex_emphasize(string: str) -> str:
    if not string.strip():
        return ""
    return r"\emph{" + string + r"}"


def latex_add_new_line(string: str) -> str:
    return string + r"\\" + "\n\t"

def latex_noindent(string:str) -> str:
    return r"\noindent " + string

def latex_underline(string: str) -> str:
    if not string.strip():
        return ""
    return r"\underline{" + string + r"}"


def latex_add_href(url: str, title: str) -> str:
    return r"\href{" + url + r"}{" + latex_underline(title) + r"}"

# add vertical space in mm
def add_space(space:int):
    return "\n" + r"\vspace{" + str(space) + "mm" + "}"+ "\n"