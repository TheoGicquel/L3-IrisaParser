# Irisa Parser Documentation

This document describes all avaiblable options for the python module `irisaparser`.

Jump to the **Example** section at the bottom to see typical usage examples.

## Command line usage

The default usage of a command is :

```sh
python3 -m irisaparser <file> [file...]
```

Without options, a command argument is interpreted as a filename. But the module allows you to use multiple options to specify program behavior.

The usage using a command with options is :

```sh
python3 -m irisaparser [[options...] [file...] ...]
```

You can pass options and files arguments in any order, but some options arguments require a second argument right after them, pay close attention to these.

Some options just change the behavior of the program and don't need further arguments, for instance :

- **`-h`** or **`--help`** : displays the help, if this option is passed, help will be displayed and no other action will be performed
- **`-t`** or **`--text`** : specify the output files format as text (enabled by default if `--xml` is not specified), may be used along with `--xml` to obtain both formats. 
- **`-x`** or **`--xml`** : specify the output files format as xml, may be used along with `--text` to obtain both format. 
- **`-s`** or **`--select`** : allows you to select which files you want to parse finally, after retrieving all files that have been passed as arguments or using the `--directory` option, this option will allow you to select which files should be extracted at the end, for more information see the **selection** section below.

*Please note that options cannot be aggregated, unlike many command line interfaces we don't allow that, for example : `-tsx` is not a valid option syntax and will instead be interpreted as a filename.*

Some other need a second argument to be defined such as :

- **`-d`** or **`--directory`** `<directorypath>` : this option allow you to specify a directory where **all** files will be parsed. This option can be used multiple times to add multiples directories to the selection. Unless you use the option `--select` to filter which files you really want to parse.

- **`-o`** or **`--output-directory`** `<directorypath>` : this option allow you to specify a directory where the created files will be placed, without this option the program will place these files in the current directory. **This option cannot be specified multiples times

Note that any of these options can be passed at any order in the command argument list. Just be aware that any non-option argument will be interpreted as a filename and that options that need a second argument will use the next passed argument. Not providing an argument after one of these options will cause the program to exit.

### About the selection.

Using the `--select` option, you will have the possibility of filter which files to finally parse, in the list you passed to the program using plain arguments or `--directory` option. All of these files will be placed in a numbered list, that you will be abble to filter using these numbers.

Note that without passing using the `--select` option, all files will be parsed, without letting you filter them.

For example using this command :

```
python3 -m irisapser fileA fileB fileC --select
```

This will allow you to select files to parses in the list you specified using command arguments.

In this part we will consider two lists, the **specified list** which contains all files specified using command arguments, and the **selected list** which contains all files you want to be parsed.

First you will be asked to choose a selection mode, there is two selection modes:

- **`e`** or **`exclude`** : At first using this mode select all files from the **specified list** and allow you to removes files from the **selected list**.

- **`i`** or **`include`**  : At first using this mode select no files in the list and allow you to add files from the **specified list** to the **selected list**.

*Note that you can switch mode at any moment to remove or add files to the **selected list***

After selecting a mode the **specified list** will be printed with an index for each file, with our example :

```
[0] fileA
[1] fileB
[2] fileC
```

Using `exclude` mode: all three files will be selected and you could removes some from the **selected list**, using `include` mode: no files will be selected and you will have to select files to be parsed.

You add or remove files using their index or a range of an inclusive range of index:

- **`<index>`** : add or remove the file from the selected list, do nothing if no file have this index. Do nothing in `include` mode if the file is already selected or in `exclude` mode if the file is already selected.

- **`<index>-<index>`** : add or remove all the files in the index range (inclusive), same behavior as unique index in case of non-existing index or already selected index.

Some examples with our three files:

With `exclude` mode:

```
[0] fileA
[1] fileB
[2] fileC

e
exclude mode selected, all files are selected at start
0
[0] fileA was removed from files to parse

Current selected files :

[1] fileB
[2] fileC
```

With `include` mode:

```
[0] fileA
[1] fileB
[2] fileC

i
include mode selected, no files selected at start
0
[0] fileA was added to the files to parse

Current selected files:

[0] fileA
```

After selecting files you can type `y` or `yes` to confirm your selection and launch the parsing task, you could also type `c` or `cancel` to cancel the selection and exit the program (yes you could also use `ctrl+C`).

At any point you could type `h` or `help` to print a simple guide on the available options you have.


## Python script usage

The `irisaparesr` module when imported in a python script using `import` keyword, will expose the following functions :

- **`parseFile`** *(`filename, [outputDir, text, xml]`)* : which parses the specfied file.
    - `filename` : relative name of the file to parse as a `string`.
    - `ouputDir` (optional) : relative path where place extracted files as a `string`. Default is current directory.
    - `text` (optional) : indicates if the file to parse will be extracted as a text file. Used as a boolean. Default is `True`.
    - `xml` (optional) : indicates if the file to parse will be extracted as a xml file. Used as boolean. Default is `False`.

*Note that if both `text` and `xml` are passed as `False`, the file will be parsed but no output file will be writed.*

- **`parseFiles`** *(`files, [outputDir, text, xml]`)* : which parse specfied files, using `parseFile` function
.
    - `files` : A list (or an equivalent `iterable`) of `string` which are names of the files to parse.
    - `ouputDir` (optional) : relative path where place extracted files as a `string`. Default is current directory.
    - `text` (optional) : indicates if files to parse will be extracted as a text file. Used as a boolean. Default is `True`.
    - `xml` (optional) : indicates if files to parse will be extracted as a xml file. Used as boolean. Default is `False`.

*Note that if both `text` and `xml` are passed as `False`, files will be parsed but no output file will be writed.* 

- **`parseArgs`** *(`args`)* : allows you to use the module in a script with all the options of the command line.
    - `args` : a list (or an equivalent `iterable`) of `string` which are arguments, to know more about arguments and avaiblables options check the **Command line usage** section above.

## Examples

There is a list of Examples of typical usage of irisaparser.

### Example 1

Here is a tree view of our files for this example:
```
├── fileA.pdf
├── fileB.pdf
└── fileC.pdf
```

- **To parse only one file:**
    ```sh
    python3 -m irisaparser fileA.pdf
    ```
    Here is a tree view of the directory after the execution:
    ```
    ├── fileA.pdf
    ├── fileA_extracted.txt
    ├── fileB.pdf
    └── fileC.pdf
    ```

- **To parse all files as xml**

    Here you have multiples options, you could use the `-d` option to pass your current directory as a directory, or specify all files one by one, or use the power of your terminal to aggregate the files for you using [wildcards](https://en.wikipedia.org/wiki/Glob_(programming)).

    To create output as xml you should add the option `-x` or `--xml`.

    - using `-d` :
    ```sh
    python3 -m irisaparser -d ./ -x
    ```

    - passing all files one by one:
    ```sh
    python3 -m irisaparser fileA.pdf fileB.pdf fileC.pdf -x
    ```

    - using [wildcards](https://en.wikipedia.org/wiki/Glob_(programming)):
    ```sh
    python3 -m irisaparser ./* -x
    ```
    Here is a tree view of the directory after the execution:
    ```
    ├── fileA.pdf
    ├── fileA_extracted.xml
    ├── fileB.pdf
    ├── fileB_extracted.xml
    ├── fileC.pdf
    └── fileC_extracted.xml
    ```

### Example 2

**Parse multiples files in multiples directories in a specified output directory**

Here is a tree view of our files for this example:
```sh
├── a.pdf
├── e.txt
├── dir1
│   ├── 1a.pdf
│   └── 1b.pdf
├── dir2
│   ├── dir2.1
│   │   ├── 21a.pdf
│   │   ├── 21b.pdf
│   │   └── 21c.pdf
│   └── dir2.2
│       ├── 22a.pdf
│       └── 22e.txt
└── out
```

Here our objective is to parse all pdf files as xml and txt and place them in the `out` directory, there are several ways to do it, but this time we will not use wildcards and just play with the command lines option.

Let's start from the simple command:
```sh
python3 -m irisaparser ./a.pdf
```

First we use the `-d` option to pass the directories with pdf files, this will work fine with `dir1` but `-d` is not recursive. So we cannot just use `-d dir2`, we need to use `-d` two more times on `dir2.1` and `dir2.2`.

The command with `-d` options:
```sh
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2
```

But `dir2.2` contains a .txt files that we don't want to parse, so we add the option `-s` to filter our selection later after the launch of the program. We will see how to use select later in this example for now here is the command:
```sh
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2 -s
```

We also want to place our output files in the directory `out` so let's use the option `-o` followed by the location of our directory:
```sh
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2 -s -o ./out
```

Finally as we want both xml and txt, we need to add both options in the command arguments `-t` and `-x`, remember by default txt format is used, passing `-x` allow to use xml format but to have both, both options need to be passed.

So here is the final command :
```sh
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2 -s -o ./out -t -x
```

Now we can use the command, press enter and it's time to remove the .txt files that we obviously don't want to parse.

*Refer to the **About selection** section of this help before processing this part of the example for more details about the selection process.*

So in our case the program will display this list of files:
```sh
[0] a.pdf
[1] 1b.pdf
[2] 1a.pdf
[3] 21b.pdf
[4] 21a.pdf
[5] 21c.pdf
[6] 22e.txt
[7] 22a.pdf
```

These are all the files we specified to the program using the command arguments, it's the **specified list**. Now The program will ask us to choose between `exclude` and `include` mode, the `exclude` mode selects by default all files and allows us to remove some files from the **selected list**, the list of tiles to actually parse. The `include` mode does the opposite, selecting no files by default and allowing you to add files from the **specified list** to the **selected list**.

So in this case we will use the `exclude` mode as we just want to remove 22e.txt, so just type `e` or `exclude` and then the index of the txt file: `6` :

```sh
e
exclude mode selected, all files are selected at start
6
[6] 22e.txt was removed from files to parse

Current selected files:

[0] a.pdf
[1] 1b.pdf
[2] 1a.pdf
[3] 21b.pdf
[4] 21a.pdf
[5] 21c.pdf
[7] 22a.pdf
```

Now just type `y` or `yes` to confir your selection and start to parse files.

Here is a tree view of our directory after the execution:
```sh
├── a.pdf
├── e.txt
├── dir1
│   ├── 1a.pdf
│   └── 1b.pdf
├── dir2
│   ├── dir2.1
│   │   ├── 21a.pdf
│   │   ├── 21b.pdf
│   │   └── 21c.pdf
│   └── dir2.2
│       ├── 22a.pdf
│       └── 22e.txt
└── out
    ├── a._extracted.txt
    ├── a._extracted.xml
    ├── 1a._extracted.txt
    ├── 1a._extracted.xml
    ├── 1b._extracted.txt
    ├── 1b._extracted.xml
    ├── 21a._extracted.txt
    ├── 21a._extracted.xml
    ├── 21b._extracted.txt
    ├── 21b._extracted.xml
    ├── 21c._extracted.txt
    ├── 21c._extracted.xml
    ├── 22a._extracted.txt
    └── 22a._extracted.xml
```

### Example 3

*Note that to use the module in a script you need to build and install it using a build utility, how to build this module as a python package is explained in the [README](https://gitlab.com/inf1603/irisaparser/-/blob/master/README.md) (The `README.md` file in the source).*

- **Parse a file using a python script**

    *The full documentation fo these functions is explained in the **Python script usage** section above*

    For this we use the `parseFile` function exposed by the module, here is a simple script to parse a file named `somepdf.pdf` located in `/tmp` using both output type, txt and xml:

    ```py
    import irisaparser # import the module

    irisaparesr.parseFile('/tmp.somepdf.pdf',xml=True);
    # note that txt is passed as True by default
    ```

- **Parse multiples files using a python script**

    For this you could use any iterable structures of string and pass it to the function `parseFile` but we will make a little utility to recursively parse all files ending by the `.pdf` extension from a directory gived as argument:

    ```py
    import irisaparser # as usual
    import os.path # to manipulate filenames and directories

    main_directory = sys.arg[1] # the first argument passed

    files = [] # list of selected files

    def select_files_from_directory(directory): # function for recursivty
        if os.path.isdir(directory): # to be sure that a directory was passed
            for file in os.listdir(directory):

                if os.isdir(file):
                    select_files_from_directory(file) # if we ancounter ta directory we call the function another time
                elif os.path.splitext(file)[1] == '.pdf':
                    files.append(file)

    select_files_from_directory(main_directory) # first call to the recursive function

    if files.count > 0: # don't parse empty list
        irisaparser.parseFiles(files) # place output txt files in current directory
    ```
    *There is multiples ways in python to parcour recursively diretories, whe choose this one because it was simple to explain for us*

- **Pass multiples options to the program using a python script**

    This function allow you to use the module like a command line utility in a python script, this word just as the command line does, just pass a `list` (or any `iterable`) of arguments as `string`, here is a simple example:

    Here we parse the file `somefile.pdf` from our current directory and place the xml output in the `/tmp` directory.

    ```py
    import irisaparser; # as needed

    arguments = ['./somefile.pdf','-o','/tmp','-x'] # arguments list

    irisaparesr.parseArgs(arguments)
    ```
    
    *Note that we don't recommend the usage of the `--select` option in a python script if it's not designed to be used in a terminal, as using this option will require user input to parse files.*