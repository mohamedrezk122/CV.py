from requests.exceptions import HTTPError
import urllib.parse
import requests
import sys 
from showinfm import show_in_file_manager  


def parse_url(tex_content:str):
    
    return urllib.parse.quote(tex_content)

def create_url(parsed_url:str) -> str:
    
    host = r"https://texlive2020.latexonline.cc/compile?text="
    return host + parsed_url


def download_pdf_file(url:str, out):

    try:
        req = requests.get(url)
        with open(f"{out}" , 'wb') as file :
            req.raise_for_status()
            print("Writing your CV..")
            file.write(req.content)
            print(f"Your CV PDF file has been written sucessfully to: \n {out}")
            show_in_file_manager(path)
    except HTTPError as err:
        print(f'A HTTPError was thrown: {err.response.status_code}')
        print("Maybe the server is down, please try again later")


