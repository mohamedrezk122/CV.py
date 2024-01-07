from termcolor import cprint
import argparse 
import os 
from api import * 
from writer import *
from reader  import *


fig = r"""
---------------------------------------------------
|            _____   __      _ __  _   _          |
|           / __\ \ / /     | '_ \| | | |         |
|          | (__ \ V /   _  | |_) | |_| |         |
|           \___| \_/   (_) | .__/ \__, |         |             
|                           |_|    |___/          |
--------------------------------------------------- 
"""


cprint(fig, 'cyan')
cprint(" \tThis script is written by Mohamed Rezk.\n", "green")


parser = argparse.ArgumentParser()  
  
parser.add_argument("input_file", help = "the path to yaml file containing the CV")  
parser.add_argument("-o", "--output", help = "file name : output file name , output.pdf by default ")  
parser.add_argument("-t", "--texfile", help = "texfile name : output.tex by default")  

args  = parser.parse_args()
cwd = os.getcwd() 

input_filepath  = args.input_file
output_filename = args.output if args.output else "output.pdf"
output_texfile = args.texfile if args.texfile else "output.tex"

def main():

    if not os.path.isdir("./output"):
        os.mkdir("./output")
    file_content_dict = load_yaml_file(input_filepath)
    content = write_tex_file(file_content_dict)
    out =  cwd+"/output/"
    if output_texfile:
        export_tex_file(content, out + output_texfile)
        
    download_pdf_file(create_url(parse_url(content)) , out+output_filename)


if __name__ == "__main__":
    main()
