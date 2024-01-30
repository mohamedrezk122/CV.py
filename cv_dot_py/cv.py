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
    default=False,
    show_default= True,
    help="Only write the tex file, NO pdf file will be produced",
)
include_tex_opt = click.option(
    "-t",
    "--tex",
    is_flag=True,
    default=False,
    show_default= True,
    help="Write tex file along with the pdf",
)
compile_locally_opt = click.option(
    "-l",
    "--local",
    help="Compile the tex file locally without an api call, you should pass a compiler, latex by default",
)


@click.command()
@filename_arg
@output_file_opt
# @config_opt
@dryrun_opt
@include_tex_opt
@compile_locally_opt
def main(filename, output, dry_run, tex, local):
    """
        "Enjoy your well-structured CV pdf file" - Mohamed Rezk
    """
    file_content_dict = load_yaml_file(filename)
    content = write_tex_file(file_content_dict)
    if any([tex, dry_run, local]) :
        export_tex_file(content, output+".tex")
    if local:
        compile_tex_locally(output, compiler=local)
    if not dry_run and not local:
        download_pdf_file(create_url(parse_url(content)), output+".pdf")

if __name__ == "__main__":
    main()
