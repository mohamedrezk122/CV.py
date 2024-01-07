import yaml
from primitives import batch_replace

DEFAULT_CONFIG_FILE = "config.yaml"


def read_config(option: str) -> dict:
    config_file_path = DEFAULT_CONFIG_FILE
    with open(config_file_path, "r") as file:
        return yaml.safe_load(file)[option]


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


# format id
FORMAT = read_config("format")
