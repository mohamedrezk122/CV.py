import yaml

from cv_dot_py.config import *
from cv_dot_py.primitives import put_error


def load_format_file(file):
    try:
        with open(f"{ROOT_DIR}/snippets/format_{FORMAT}/{file}.tex", "r") as f:
            return f.read()
    except:
        put_error("Cannot find {file} format found")


def load_yaml_file(file_path):
    with open(file_path, "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            return exc
