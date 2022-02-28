# Irisa Parser

Python script to parse pdf files into text files.

## Setup

you can get the latest stable version by cloning the `master` branch of our repository with :
```sh
git clone https://gitlab.com/inf1603/irisaparser.git
```

Make sure that Python and Pip are installed on your computer.

### Software Requirements:

 - Python `>3.10`
 - Pip `22.0`
 - Java `>7`


### Pip packages:

Once all software requirements are satisfied, please make to sure to install the following pip packages :
To install pipy packages make sure that pip is intalled and use :

```sh
pip install <packagename>
```

The following depencies are required :

 - [**pdfplumber**](https://pypi.org/project/pdfplumber/) 0.6.0
 - [**tika**](https://pypi.org/project/tika/) 1.24
 - [**spacy**](https://pypi.org/project/spacy/) 3.2.2
 - [**colorama**](https://pypi.org/project/colorama/) 0.4.4

You can also install every dependency in one go with :
```python
pip install pdfplumber tika spacy colorama
```

## Usage

To parse a pdf file use the command:

```sh
python3 ./irisaparser/cli.py <args>
```
For example to parse a file named `f1.pdf` located in `/home/user/pdfs/` and to output results in `/tmp`, use:

```sh
python3 ./irisaparser/cli.py /home/user/pdfs/f1.pdf -o /tmp
```

To parse all the files located in `/home/user/pdfs`, use:

```sh
python3 ./irisaparser/cli.py -d /home/user/pdfs
```

Note that if no output directory is provided using `-o`, text files will be placed **in current directory**.

For more information about how to use `cli.py` type the following command:

```sh
python3 ./irisaparser/cli.py --help
```