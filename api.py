import os
import requests
import requests_cache
import urllib.parse

from primitives import put_error, put_success

def parse_url(tex_content: str):
    return urllib.parse.quote(tex_content)

def create_url(parsed_url: str) -> str:
    host = r"https://texlive2020.latexonline.cc/compile?text="
    return host + parsed_url

def download_pdf_file(url: str, out):
    try:
        # caching requests, less time
        # cache will be written in cache dir ~/.cache in case of linux 
        cached_session = requests_cache.CachedSession('cached_session', use_cache_dir=True)
        req = cached_session.get(url, timeout=10)
        with open(f"{out}", "wb") as file:
            req.raise_for_status()
            print("Writing your CV..")
            file.write(req.content)
            put_success(f"Your PDF file has been written sucessfully to: \n {out}")
    except requests.exceptions.Timeout:
        put_error("Timed out")
    except requests.exceptions.HTTPError:
        put_error(f"Maybe the server is down, please try again later")
