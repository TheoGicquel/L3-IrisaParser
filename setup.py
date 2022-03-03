from setuptools import setup

setup(
    name = "irisaparser",
    version = "1.0",
    packages = ['.irisaparser'],
    description = "Extract text from pdf files",
    install_requires = [
        "pdfbplumber >= 0.6.0",
        "tika >= 1.24",
        "spacy >= 3.2.2",
        "colorama >= 0.4.4",
    ],
    python_requires = '>=3.10'
)