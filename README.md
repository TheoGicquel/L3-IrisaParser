# Irisa Parser

Python script to parse pdf files into text files.

## Setup

You can get the latest stable version by cloning the `master` branch of our repository with :
```sh
git clone https://gitlab.com/inf1603/irisaparser.git
```

For other version please consult the [release section](https://gitlab.com/inf1603/irisaparser/-/releases) of the repository on gitlab, and download the source archive corresponding to the desired version.

Make sure that Python and Pip are installed on your computer.

### Software Requirements:

 - Python `>3.10`
 - Pip `22.0`
 - Java `>7`


### Pip packages *(optional)*:

*This step is necessary only if you don't want to build the package yourself, if you don't want to install manually these dependencies, jump to the **Build** section.*

Once all software requirements are satisfied, please install the following pip packages :
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

**/!\\ At first usage, the module will download tika java package, this may take a lot of time. /!\\**

*Note that you must have the dependencies of the **Pip package** section to use irisaparser this way, if it's not the case please see the **Build** section or consult the **Pip package** section.*

Make sure you are placed above the `irisaparser` directory, or for more conveniance build the package.

To parse a pdf file use the command:

```sh
python3 -m irisaparser <args>
```

For example to parse a file named `f1.pdf` located in `/home/user/pdfs/` and to output results in `/tmp`, use:

```sh
python3 -m irisaparser /home/user/pdfs/f1.pdf -o /tmp
```

To parse all the files located in `/home/user/pdfs`, use:

```sh
python3 -m irisaparser -d /home/user/pdfs
```

Note that if no output directory is provided using `-o`, text files will be placed **in current directory**.

For more information about how to use module type the following command:

```sh
python3 -m irisaparser --help
```

## Build

Make sure that you have [**setuptools**](https://pypi.org/project/setuptools/) and [**wheel**](https://pypi.org/project/wheel/) on your system, you can install these depencies with the command:

```sh
pip install setuptools wheel
```

To build the package make sure that you are above the `irisaparser` directory and use the following command:

```sh
python3 setup.py bdist_wheel
```
*for more information about this command consult the [documentation](https://wheel.readthedocs.io/en/stable/)*

To install your package, use the following command with the .whl file you just built:

```sh
pip install <some .whl file>
```

## Package usage

**/!\\ At first usage, the module will download tika java package, this may take a lot of time. /!\\**

Once you have installed the package, you can use it with the following command everywhere:
```sh
python3 -m irisaparser <args>
```

Also you can import the package in a python script like that:
```py
import irisaparser

# parse a file and put the output in the specified directory:
irisaparser.parseFile("filename","./out")

# parse a file and put the xml output in the current directory:
irisaparser.parseFile("filename",xml=True)

# parse multiple files provided in the list parameter files:
filesnames = ["file1","file2"]
irisaparser.parseFiles(filenames)

# do the equivalent of the command line usage, just pass the arguments as a list of strings:
args = ["-d","./Corpus_2021","-o","./out"]
irisaparser.parseArgs(args)

```

## Documentation

For more information about the different options and behaviors of the program consult our [documentation](https://gitlab.com/inf1603/irisaparser/-/blob/master/DOC.md) page (The `DOC.md` if you downloaded the source code).