import os
from setuptools import setup

print(os.getcwd())

def get_model_files():
    files = []
    for (path, directories, filenames) in os.walk('./irisaparser/CustomNER'):
        for filename in filenames:
            files.append(os.path.join('..', path, filename))
    return files

setup(
    name = "irisaparser",
    version = "1.0",
    packages = ['irisaparser'],
    package_data={'irisaparser':get_model_files()},
    description = "Extract text from pdf files",
    install_requires = [
        "pdfplumber >= 0.6.0",
        "tika >= 1.24",
        "spacy >= 3.2.2",
        "colorama >= 0.4.4",
    ],
    python_requires = '>=3.10'
)