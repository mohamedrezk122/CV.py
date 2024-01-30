#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="CV.py",
    version="0.1",
    description="Create your LaTeX CV with yaml without a LaTeX compiler",
    author="Mohamed Rezk",
    author_email="mohrizq895@gmail.com",
    url="https://github.com/mohamedrezk122/CV.py",
    packages=find_packages(),
    py_modules=["cv_dot_py"],
    include_package_data=True,
    install_requires=["Click", "pyyaml", "termcolor", "requests-cache", "pathlib"],
    entry_points="""
    [console_scripts]
    cv-dot-py=cv_dot_py.cv:main
    """,
)
