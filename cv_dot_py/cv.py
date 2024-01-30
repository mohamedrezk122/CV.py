import os
import click
from termcolor import cprint

from cv_dot_py.writer import export_tex_file
from cv_dot_py.writer import write_tex_file
from cv_dot_py.reader import load_yaml_file
from cv_dot_py.api import *


# fig = r"""
# ---------------------------------------------------
# |            _____   __      _ __  _   _          |
# |           / __\ \ / /     | '_ \| | | |         |
# |          | (__ \ V /   _  | |_) | |_| |         |
# |           \___| \_/   (_) | .__/ \__, |         |             
# |                           |_|    |___/          |
# --------------------------------------------------- 
# """

# cprint(fig, "cyan")
# cprint("This script is written by Mohamed Rezk.\n", "green")


# parser = argparse.ArgumentParser()

# parser.add_argument("input_file", help="the path to yaml file containing the CV")
# parser.add_argument(
#     "-o", "--output", help="file name : output file name , output.pdf by default "
# )
# parser.add_argument("-t", "--texfile", help="texfile name : output.tex by default")

# args = parser.parse_args()
# cwd = os.getcwd()

# input_filepath = args.input_file
# output_filename = args.output if args.output else "output.pdf"
# output_texfile = args.texfile if args.texfile else "output.tex"


filename_arg = click.argument("filename", required=True, type=click.Path(exists=True))
output_file_opt = click.option(
    "-o",
    "--output",
    default="output",
    show_default=True,
    type=click.Path(),
    help="Output file path, default output.pdf",
)
config_opt = click.option(
    "-c",
    "--config",
    type=click.Path(exists=True),
    default="config.yaml",
    show_default=True,
    help="Configuration file path if not specified the default configs will be loaded",
)
dryrun_opt = click.option(
    "-d",
    "--dry_run",
    is_flag=True,
    help="Only write the tex file, NO pdf file will be produced",
)
include_tex_opt = click.option(
    "-t",
    "--tex",
    is_flag=True,
    help="Write tex file along with the pdf",
)


@click.command()
@filename_arg
@output_file_opt
# @config_opt
@dryrun_opt
@include_tex_opt
def main(filename, output, dry_run, tex):
    file_content_dict = load_yaml_file(filename)
    content = write_tex_file(file_content_dict)
    if not dry_run :
        download_pdf_file(create_url(parse_url(content)), output+".pdf")
    if tex or dry_run :
        export_tex_file(content, output+".tex")

if __name__ == "__main__":
    main()
