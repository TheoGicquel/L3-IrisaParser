# Irisa Parser

Python script to parse pdf files into text files.

## Setup

Clone this repository, use the `master` branch.

Make sure that Python and Pip are installed on your computer.

### Softwares Requirements:

 - Python `3.10 +`
 - Pip `22.0`
 - Java `7 +`

### Pip packages:

After make to sure to install the following pip packages.
To install pipy packages make sure that pip is intalled and use :

```sh
pip install <packagename>
```

Theses depencies are required :

 - [**pdfplumber**](https://pypi.org/project/pdfplumber/) 0.6.0
 - [**tika**](https://pypi.org/project/tika/) 1.24
 - [**spacy**](https://pypi.org/project/spacy/) 3.2.2
 - [**colorama**](https://pypi.org/project/colorama/) 0.4.4

## Usage

Make sure to be in the folder `irisaparser` (at the same level of `cli.py` file).

To parse a pdf file use this command:µ

```sh
py ./cli.py <args>
```

For example to parse a file called `f1.pdf` located in `/home/user/pdfs/` and to place the output in `/tmp`, use:

```sh
py ./cli.py /home/user/pdfs/f1.pdf -o /tmp
```

To parse all the files located in `/home/user/pdfs`, use:

```sh
py ./cli.py -d /home/user/pdfs
```

Note that if no output directory is provided using `-o`, text files will be placed in current directory.

For more information about how using `cli.py` type the following command:

```sh
py ./cli.py --help
```