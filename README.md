# CV.py
<p align="center"><img src="https://user-images.githubusercontent.com/50466262/218974424-28ddff01-76d2-4258-bda0-3b89cdbea5d3.png" /></p>

``` CV.py```  is  a simple conversion of yaml file which contains the CV information in a hierarchical order to nice and elegant LaTeX file that is fed to an API for compilation. And you have your CV PDF file on local machine as simple as that. The main point is that you do not have to have LaTeX or know how it is written , just enjoy the good-looking , well-structured, and fault-proof PDF file. 

## Requirements 

- [Python 3](https://www.python.org/downloads/)  and pip 
- All other required dependencies can be installed through the following command, open ```cmd```  if you are on Windows, or ```terminal``` if you are Linux, Mac, or BSD. 

``` sh
$ pip install -r requirements.txt
```

## Features 

- [x] Supports multiple formats through snippets directory 
- [x] supports URL (hyperlinks) embedding inside description body 

## Usage

You can use the following command for help :
``` shell
python3 cv.py -h 
```

The script can be used as follows:
``` shell
python3 cv.py input.yaml -o output.pdf -t output.tex
```

However, ```-o``` and ```-t``` are optional arguments , if they are not specified  like the command below , the script generates the PDF file under the name of  ```output.pdf``` likewise,  ```output.tex```.    

``` shell
python3 cv.py input.yaml 
```

All output files will be written in ```output/``` directory (folder), which will be generated by the script.

## yaml file format

Please browse ```template.yaml``` for additional help on  how the yaml file is properly formatted, also you can see the corresponding PDF file produced by the script under the name ```template.pdf```
The supported structure of the file:

```info```, ```section```, ```entry``` , ```multicol```

###  ```info```  field 

- it is one-time field (written once)
- name is a required parameter 
- you can add any number of information points / keys (like phone, work phone, etc.) 
- points under ```url``` key takes the name of key and embed  the corresponding URL inside the key like so ("https://github.com/mohamedrezk122")[Github] 

```yaml
info:
  name: "Mohamed Mahmoud Rezk "
  phone: "01222448102"
  email: "mohrizq895@gmail.com"
  secondemail: "2002114@eng.asu.edu.eg"
  url:
    LinkedIn: "https://www.linkedin.com/in/mohamed-m-rezk/"
    Github: "https://github.com/mohamedrezk122"
    Blog : "https://mohamedrezk122.github.io/"
```

###  ```section```  field 

- section has to be unique , meaning no  two section have the same name , it shall take the form ```section+digit```  like ```section1``` or ```section+digit+digit``` like ```section12``` , these are the accepted formats.  
- section must have ```title``` key
- under section you can use either ```entry```  or ```multicol``` ( discussed below)

``` yaml
section2 :
  title :   Experience 
  entry1 : 
    title: "Research Intern"
    org:  "ASU - Dynamic Systems and Digitalisation Cluster"
    year: "Aug-Oct-2022"
    points:
      a: "Project title:Mapping of artificial acoustic emission sources on wind turbine blades "
      b: "I implemented several optimization see algorithms with some bench-markings like:"
      c: "- Particle Swarm Optimization"
      d: "- Simulated Annealing"
      e: "- Simplex (Nelder-Mead) Method"
      f: "see [code]"
    url:
      code: "https://github.com/mohamedrezk122/AE-software"
```

###  ```entry```  field 

- entry has to be unique within the same section , meaning no  two entries have the same name under the same section , it shall take the form ```entry+digit```  like ```entry1``` or ```entry+digit+digit``` like ```entry12``` , these are the accepted formats.  
- entry must have ```title``` key
- the accepted  ```entry``` attributes are  ```title``` , ```org``` , ```year```,```points```,```url```

``` yaml
section2 :
  title :   Experience 
  entry1 : 
    title: "Research Intern"
    org:  "ASU - Dynamic Systems and Digitalisation Cluster"
    year: "Aug-Oct-2022"
    points:
      a: "Project title:Mapping of artificial acoustic emission sources on wind turbine blades "
      b: "I implemented several optimization see algorithms with some bench-markings like:"
      c: "- Particle Swarm Optimization"
      d: "- Simulated Annealing"
      e: "- Simplex (Nelder-Mead) Method"
      f: "see [code]"
    url:
      code: "https://github.com/mohamedrezk122/AE-software"
```

###  ```multicol```  field 

- multicol has to be unique within the same section , meaning no  two multicol fields have the same name under the same section , it shall take the form ```multicol+digit```  like ```multicol1``` or ```multicol+digit+digit``` like ```multicol12``` , these are the accepted format.  
- the accepted  ```entry``` attributes are  ```ncols``` ,```points```
- if ```ncols``` is not specified , it is 3 by default.

``` yaml
section3:
  title: Skills

  multicol1:
    cols: 3
    points:
      a: HTML
      b: CSS
      c: Vanilla JS
      d: SCSS
      e: Node.js
      f: React.js
      g: Three.js
      h: Electron.js
      k: Version Control (git)
      h: Responisve Design
      s: MySQL
```
## Notes and limitations 

- if there is a ```:``` , colon inside the text your writing inside the yaml file you have to put the whole string inside quotations like so  ```"some text : some text"```
- if you violated the naming convention of entry, section, or multicol, the field will not be written to the PDF file so double check.
- if two same-level fields have the same name the latter only will be written.
- the order used by the script is positional order meaning that regardless the digit in front of the field , the script processes the file in a chronological order.
- if there is a ```$``` , ```&``` or ```%``` you need to escape them and put the whole string in ```""``` like so ```"some text  \\$ some text"```
 