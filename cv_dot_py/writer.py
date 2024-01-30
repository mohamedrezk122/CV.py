import re
from typing import Any

from cv_dot_py.config import *
from cv_dot_py.reader import *
from cv_dot_py.primitives import *


INFO_SEP = " | "


def write_info(info_dict: dict) -> str:
    info_template = load_format_file("info")

    if info_dict.get("name", 0):
        name = info_dict["name"]
    else:
        name = "NAME PLACE HOLDER"
        put_warning("No Name")

    points_string = ""
    for title in info_dict["url"]:
        points_string += (
            latex_add_href(url=info_dict["url"][title], title=title) + INFO_SEP
        )

    for i, point in enumerate(info_dict):
        if point in {"name", "url"} or not info_dict[point]:
            continue
        points_string += str(info_dict[point])
        if i == len(info_dict) - 1:
            break
        points_string += INFO_SEP

    replacements = {"[[points]]": points_string, "[[name]]": name}

    return batch_replace(info_template, replacements)


def write_section(title: str) -> str:
    return  "\n" + r"\Title{" + title + "}\n"


def write_url(entry: dict, content: str) -> str:
    if not entry.get("url", 0):
        return content
    for title in entry["url"]:
        link = latex_add_href(url=entry["url"][title], title=title)
        content = content.replace(f"[{title}]", link)
    return content


def write_generic_entry(
    title: str, year: str, org: str = "", points: dict = None
) -> str:
    if not points:
        return ""

    date = r"\Date{" + year +"}\n"
    if org :
        org = latex_add_new_line(latex_emphasize(org)) 
    points_string = "".join([latex_add_new_line(points[point]) for point in list(points.keys())[:-1]])
    points_string += points[list(points.keys())[-1]]
    entry = r"\Entry"+ "\n\t{" + title + "}\n\t{" + org + points_string + "\n}\n"
    return date + entry


def write_column_entry(width: int, points: dict) -> str:
    if not points:
        return ""

    col_template = load_format_file("col")
    points_string = "".join([latex_add_new_line(points[point]) for point in points])
    replacements = {"[[col_width]]": width, "[[points]]": points_string}
    return batch_replace(col_template, replacements)


def write_multi_column_entry(ncols: int, points: dict) -> str:
    multi_col_template = ""
    idx = len(points) // ncols

    for i in range(ncols):
        u = idx * (i + 1) if i < ncols - 1 else len(points)
        multi_col_template += write_column_entry(
             '%.3f'%(1 / ncols), dict(list(points.items())[idx * i : u])
        )

    return multi_col_template


def get_value_or_default(field: dict, key: str, default: Any = "") -> Any:
    value = default
    if field.get(key, 0):
        value = field[key]
    return value


def append_multicol(subfield: dict, tex_content: str) -> str:
    cols = get_value_or_default(subfield, "cols", 3)
    points = get_value_or_default(subfield, "points", None)
    return tex_content + write_multi_column_entry(cols, points)


def append_entry(subfield: dict, tex_content: str) -> str:
    year = get_value_or_default(subfield, "year")
    org = get_value_or_default(subfield, "org")
    points = get_value_or_default(subfield, "points", None)
    entry_content = write_generic_entry(subfield["title"], year, org, points)
    entry_content = write_url(subfield, entry_content)
    return tex_content + entry_content

def write_tex_header():
    file_header = load_format_file("header")
    date_macro = load_format_file("date")
    entry_macro = load_format_file("entry")
    title_macro = load_format_file("section").replace("[[BAR]]", 
        str(int(INCLUDE_BAR))).replace("[[SEP]]", add_space(SECTION_ENTRY_SEP))
    return file_header.replace("[[macros]]", title_macro+date_macro+entry_macro)

def write_tex_file(file_content: dict) -> str:
    section_pattern = re.compile(r"section\d+")
    entry_pattern = re.compile(r"entry\d+")
    multicol_pattern = re.compile(r"multicol\d+")

    file_header= write_tex_header()    
    file_header = adjust_document_margins(file_header)
    tex_content = ""

    if file_content.get("info", 0):
        tex_content += write_info(file_content["info"])
        tex_content += add_space(AFTER_INFO_SEP)
    else:
        put_warning("No information section")

    try:
        file_content.pop("info")
        for i,field in enumerate(file_content):
            if not bool(section_pattern.match(field)):
                continue
            if i != 0:
                tex_content += add_space(SECTION_SECTION_SEP)
            tex_content += write_section(file_content[field]["title"])
            if len(field) < 2:
                continue

            for j,sub in enumerate(file_content[field]):
                subfield = file_content[field][sub]
                if bool(entry_pattern.match(sub)):
                    tex_content = append_entry(subfield, tex_content)
                elif bool(multicol_pattern.match(sub)):
                    tex_content = append_multicol(subfield, tex_content)
                if j not in {0, len(file_content[field])-1}:
                    tex_content += add_space(ENTRY_ENTRY_SEP)

    except:
        put_error("Not able to process yaml data, please check the file")

    return file_header.replace("[[content]]", tex_content)

def export_tex_file(content: str, file_path: str):
    try:
        with open(f"{file_path}", "w") as file:
            file.write(content)
            put_success(f"Your texfile has been written sucessfully to:\n {file_path}")
    except:
        put_error("Cannot access directory to write your texfile")
