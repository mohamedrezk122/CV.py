import yaml
from pathlib import Path

from cv_dot_py.primitives import batch_replace

ROOT_DIR = Path(__file__).parent.parent
DEFAULT_CONFIG_FILE = ROOT_DIR.joinpath('config.yaml')

config_content = None

def read_config(option: str) -> dict:
    global config_content
    # avoid reptitve calls to io 
    if config_content :
        return config_content[option] 
    config_file_path = DEFAULT_CONFIG_FILE
    with open(config_file_path, "r") as file:
        config_content = yaml.safe_load(file)
        return config_content[option]

def adjust_document_margins(header: str) -> str:
    margins = read_config("margins")
    replacements = {
        "[[left]]": margins["left"],
        "[[right]]": margins["right"],
        "[[top]]": margins["top"],
        "[[bottom]]": margins["bottom"],
        "[[unit]]": margins["unit"],
    }
    return batch_replace(header, replacements)

def adjust_document_geometry(header:str) -> str:
    geometry = read_config("geometry")
    replacements = {
        "[[width]]": geometry["width"],
        "[[height]]": geometry["height"],
        "[[g_unit]]": geometry["unit"],
    }
    return batch_replace(header, replacements)    

# format id
FORMAT = read_config("format")
SECTION_ENTRY_SEP = read_config("section_entry_separation")
SECTION_SECTION_SEP = read_config("section_section_separation")
ENTRY_ENTRY_SEP = read_config("entry_entry_separation")
AFTER_INFO_SEP = read_config("after_info_separation")
INCLUDE_BAR = read_config("add_bar_next_to_section_title")
