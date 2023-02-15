import yaml
import re 
from api import * 
from config import * 

def load_format_file(file):
    try :
        with open(f"./snippets/format_{FORMAT}/{file}.tex" , "r") as f :
            return f.read()
    except:
        print("No format file found, it might be deleted. Consider download the file from the project's repo")

def load_yaml_file(file_path):

    with open(file_path , 'r') as file :
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            return exc

def adjust_document_geometry(header:str)-> str:
    
    try:
        left = str(LEFT_MARGIN)    
    except:
        left = "1.524"
    try:
        right = str(RIGHT_MARGIN)    
    except:
        right = "1.524"
    try:
        top = str(TOP_MARGIN)    
    except:
        top = "1.27"
    try:
        bottom = str(BOTTOM_MARGIN)    
    except:
        bottom = "1.524"

    replacements = { "[left]"  : left , 
                     "[right]" : right,
                     "[top]"   : top  , 
                     "[bottom]": bottom}

    for i in replacements :
        header = header.replace(i , replacements[i])

    return header 

def write_info( name:str , points:dict)-> str :
    
    info_template = load_format_file("info")
    points_string =""
    if points["url"] : 
        for url in points["url"]:
            points_string += r"\href{[point]}{\underline{[title]}}".replace(
                                                                "[title]" , str(url)).replace(
                                                                "[point]", str(points['url'][url])) + " | "
        points.pop("url")
    for point in points : 
        if points[point] is not None :
            points_string += str(points[point]) + r" | "

    points_string = points_string[:-3]
    return info_template.replace(
                                "[points]" , points_string).replace(
                                "[name]" , name)

def write_section(title:str) -> str:

    section_template = load_format_file("section")
    return section_template.replace('[title]' , title)

def write_url(entry:dict, content:str):

    try:
        for url in entry["url"] :
            link = r"\href{[url]}{\underline{[title]}}".replace("[title]" ,
                             url).replace("[url]", entry["url"][url])
            content = content.replace(f"[{url}]" , link)
    
    except:
        pass
    return content

def write_generic_entry( title:str,  year:str,
                         org="", points:dict=None )-> str:
    
    entry_template = load_format_file("entry")
    if org not in  ["" , " " ]:
        org = r"\emph{"+ org +  r"}\\"
    points_string = ""
    if points is not None:
        
        for point in points:
            points_string +=  points[point] + r"\\"
            # points_string += "\n\t" 

    replacements = { "[title]" : title , 
                     "[year]"  : year  ,
                     "[org]"   : org   ,
                     "[points]": points_string}

    for i in replacements :
        entry_template = entry_template.replace(i , replacements[i])

    return entry_template

def write_column_entry(width:int , points:dict) -> str:

    col_template = load_format_file("col")
    points_string = ""
    if points is not None:
        for point in points:
            # points_string += "- "
            points_string += points[point] + r"\\"

    replacements = { "[col_width]" : str(width) , 
                     "[points]": points_string}

    for i in replacements :
        col_template = col_template.replace(i , replacements[i])

    return col_template 

def write_multi_column_entry(ncols:int, points:dict) -> str:

    multi_col_template = ""
    idx = len(points) // ncols 

    for i in range(ncols):
        u = idx*(i+1) if i < ncols-1 else len(points)
        multi_col_template += write_column_entry(1/ncols , 
                                    dict(list(points.items())[idx*i:u]))

    return multi_col_template


def write_tex_file(file_content:dict)-> str :
    
    file_header = load_format_file("header")
    file_header = adjust_document_geometry(file_header)
    tex_content = ""
    try:
        tex_content  += write_info(
                    file_content['info']['name'],
                    dict(list(file_content['info'].items())[1:]))
        # print(tex_content)
    except:
        print("No Name or enough personal information in CV yaml file")

    try:
        file_content.pop('info')
        section_pattern = re.compile(r'section[\d , \d\d]')
        entry_pattern = re.compile(r'entry[\d , \d\d]')
        multicol_pattern = re.compile(r'multicol[\d , \d\d]')

        for field in file_content : 
            if bool(section_pattern.match(field)) :
                tex_content += write_section(file_content[field]["title"])
                if len(field) >= 2 : 
                    for sub in file_content[field] :
                        if bool(entry_pattern.match(sub)):
                            
                            subfield = file_content[field][sub] 
                            try:
                                year =  subfield["year"] 
                            except :
                                year =  ""

                            try:
                                org =  subfield["org"] 
                            except :
                                org =  ""
                            try:
                                points =  subfield["points"] 
                            except :
                                points =  None
                            entry_content  = write_generic_entry(subfield["title"] , year ,  org , points)
                            entry_content  = write_url(subfield , entry_content)
                            tex_content+= entry_content 
                        elif bool(multicol_pattern.match(sub)):
                            subfield = file_content[field][sub] 
                            try:
                                cols =  subfield["cols"] 
                            except :
                                cols = 3
                            try:
                                points =  subfield["points"] 
                            except :
                                points =  None
                            tex_content += write_multi_column_entry(cols , points)

        return file_header.replace("[content]" , tex_content)
    except:
        print("not able to process yaml data , please check the file and try again")


def export_tex_file(content:str , file_path:str) :
    
    try:
        with open(f"{file_path}", "w") as file: 
            file.write(content)
            print(f"Your texfile has been written sucessfully to:\n {file_path} ")
    except:
        print("cannot access directory to write your texfile")

