# IrisaParser Documentation

This document describes all available options for the python module `irisaparser`.

Jump to the **Example** section to view typical usage examples.

- [IrisaParser Documentation](#irisaparser-documentation)
  - [Command line usage](#command-line-usage)
    - [Default usage](#default-usage)
    - [About selection](#about-selection)
    - [Quick demonstration](#quick-demonstration)
  - [Examples](#examples)
    - [Example 1](#example-1)
    - [Example 2](#example-2)
    - [Example 3](#example-3)

---

## Command line usage

### Default usage

The default usage of a command is :

```shell
python3 -m irisaparser <file> [file...]
```

Without options, a command argument is interpreted as a filename. However the module allows using multiple options to specify program behavior.

The typical command using options is :

```shell
python3 -m irisaparser [[options...] [file...] ...]
```

You can pass options and files arguments in any order, but some options arguments require a second argument right after them, pay close attention to these.

Some options simply change the behavior of the program and don't need further arguments, for instance :

- **`-h`** or **`--help`** : displays the help, if this option is passed, help will be displayed and no other action will be performed
- **`-t`** or **`--text`** : specify the output files format as text (enabled by default if `--xml` is not specified), may be used along with `--xml` to obtain both formats.
- **`-x`** or **`--xml`** : specify the output files format as xml, may be used along with `--text` to obtain both format.
- **`-s`** or **`--select`** : allows you to select which files you want to parse finally, after retrieving all files that have been passed as arguments or using the `--directory` option, this option will allow you to select which files should be extracted at the end, for more information see the **selection** section below.

*Please note that options cannot be aggregated, unlike many command line interfaces we do not allow that, for instance : `-tsx` is not a valid option syntax and will instead be interpreted as a filename.*

Some other need a second argument to be defined, such as :

- **`-d`** or **`--directory`** `<directorypath>` : this option allows specifying a directory where **all** files will be parsed. This option can be used multiple times to add multiple directories to the selection. Unless you use the option `--select` to filter exactly which files you really want to parse.

- **`-o`** or **`--output-directory`** `<directorypath>` : this option allow you to specify a directory where the output files will be placed, without this option the program will place these files in the current directory. **This option can only be specified once**

Note that any of these options can be passed in any order in the command argument list. Just be aware that any non-option argument will be interpreted as a filename, and that options that need a second argument will use the next passed argument. Not providing an argument after one of these options will cause the program to exit.

### About selection

Using the `--select` option allows filtering which files to finally parse, in the list you passed to the program using plain arguments or `--directory` option.
All these files will be placed in a numbered list, that you will be able to filter using these numbers.

Note that not using the `--select` option will cause every file to be parsed without filtering.

For example using this command :

```shell
python3 -m irisapser fileA fileB fileC --select
```

This will allow you to select which files to parse in the list you specified using command arguments.

### Quick demonstration

In this part we will consider two lists, the **specified list** which contains all files specified using command arguments, and the **selected list** which contains all files we wish to parse.

First you will be asked to choose a selection mode, there are two selection modes available:

- **`e`** or **`exclude`** : using this mode selects every file from the **specified list** and allows you to remove files from the **selected list** as needed.

- **`i`** or **`include`**  : using this mode selects none of the files from the list and allow you to add files from the **specified list** into the **selected list**.

*Note that you can switch mode at any moment to remove or add files to the **selected list***

After selecting a mode the **specified list** will be printed with an index for each file, for instance, using the example from above :

```shell
[0] fileA
[1] fileB
[2] fileC
```

Using `exclude` mode: all three files will be selected and you could removes some from the **selected list**, using `include` mode: no files will be selected and you will have to select which files should be parsed.

You add or remove files using their index or a range of an inclusive range of index:

- **`<index>`** : add or remove a file from the selected list, does nothing if no file corresponds to the index. Does nothing if the file is already selected.

- **`<index>-<index>`** : add or remove all the files in index range (inclusive), same behavior as unique index in case of non-existing index or already selected index.

Some examples with our three files from above:

With `exclude` mode:

```shell
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

```shell
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

After selecting files you can type `y` or `yes` to confirm your selection and launch the parsing task, you can also type `c` or `cancel` to cancel the selection and exit the program (`ctrl+C` also works).

At any point you can type `h` or `help` to print a simple guide on the available options.

## Examples

There is a list of Examples of typical usage of irisaparser.

### Example 1

Here is a tree view of our files for this example:

```tree
├── fileA.pdf
├── fileB.pdf
└── fileC.pdf
```

- **To parse only one file:**

    ```shell
    python3 -m irisaparser fileA.pdf
    ```

    Here is a tree view of the directory after the execution:

    ```tree
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

    ```tree
    ├── fileA.pdf
    ├── fileA_extracted.xml
    ├── fileB.pdf
    ├── fileB_extracted.xml
    ├── fileC.pdf
    └── fileC_extracted.xml
    ```

### Example 2

> **Parse multiples files in multiples directories into a specified output directory**

Here is a tree view of the files for this example:

```tree
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

Here our objective is to parse all pdf files as XML and plain text and place our results in the `out` directory, there are several ways to do this, but this time we will not use wildcards and instead just play with the command lines option.

Let's start from a simple command:

```shell
python3 -m irisaparser ./a.pdf
```

First we use the `-d` option to use the directories with pdf files, this will work fine with `dir1` but `-d` is not recursive. So we cannot just use `-d dir2`, we need to use `-d` two more times on `dir2.1` and `dir2.2`.

We now have our `-d` options:

```shell
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2
```

However, `dir2.2` contains a .txt files that we do not wish to parse, so we add the option `-s` to filter our selection after launching the parser. We will see how to use select later in this example for now here is the command:

```shell
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2 -s
```

We also want to place our output files in the `out` directory so let's use the option `-o` followed by the path of `out`:

```shell
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2 -s -o ./out
```

Finally as we want both xml and txt, we need to add both options in the command arguments `-t` and `-x`, remember : by default the plain text format is used, passing `-x` allow to use XML formatting but to have both, both options need to be used.

So here is the final command :

```shell
python3 -m irisaparser ./a.pdf -d ./dir1 -d ./dir2/dir2.1 -d ./dir2/dir2.2 -s -o ./out -t -x
```

Now we can use the command, press enter and it is time to remove the .txt files that we obviously don't want to parse.

*Refer to the **About selection** section of this help before processing this part of the example for more details about the selection process.*

So in our case the program will display this list of files:

```shell
[0] a.pdf
[1] 1b.pdf
[2] 1a.pdf
[3] 21b.pdf
[4] 21a.pdf
[5] 21c.pdf
[6] 22e.txt
[7] 22a.pdf
```

These are all the files we previously specified to the program using the command arguments, it's the **specified list**. Now The program will ask us to choose between the `exclude` and `include` mode, the `exclude` mode selects by default all files and allows us to remove some files from the **selected list**( the list of files to actually parse). The `include` mode does the opposite by selecting no files by default and allowing you to add files from the **specified list** to the **selected list**.

So in this case we will use the `exclude` mode as we just want to remove `22e.txt`, so just type `e` or `exclude` and then the index of the txt file: `6` :

```shell
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

Now just type `y` or `yes` to confirm your selection and start to parse files.

Here is a tree view of our directory after the execution:

```shell
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

    To do this we use the `parseFile` method exposed by the module, here is a simple script to parse a file named `somepdf.pdf` located in `/tmp` using both output type, txt and XML:

    ```py
    import irisaparser # import the module

    irisaparesr.parseFile('/tmp.somepdf.pdf',xml=True);
    # note that txt is passed as True by default
    ```

- **Parse multiples files using a python script**

    For this you could use any iterable structure of strings and pass it to the function `parseFile` however we will create a little utility to recursively parse all files ending with the `.pdf` extension from a directory given as argument:

    ```py
    import irisaparser # as usual
    import os.path # to manipulate filenames and directories

    main_directory = sys.arg[1] # the first argument passed

    files = [] # list of selected files

    def select_files_from_directory(directory): # function to call for recursivly
        if os.path.isdir(directory): # to be sure that a directory was passed
            for file in os.listdir(directory):

                if os.isdir(file):
                    select_files_from_directory(file) # if we encounter the directory we call the function once more
                elif os.path.splitext(file)[1] == '.pdf':
                    files.append(file)

    select_files_from_directory(main_directory) # first call to the recursive function

    if files.count > 0: # do not parse empty list
        irisaparser.parseFiles(files) # place output txt files in current directory
    ```

    *There are multiple ways in python to go recursively through directories, whe chose this one because it was simpler to explain*

- **Pass multiples options to the program using a python script**

    This function allows you to use the module like a command line utility inside a python script, this works in the same way as the command line, just pass a `list` (or any `iterable`) of arguments as `string`, here is a simple example:

    Here we parse the file `somefile.pdf` from our current directory and place the xml output in the `/tmp` directory.

    ```py
    import irisaparser; # as needed

    arguments = ['./somefile.pdf','-o','/tmp','-x'] # arguments list

    irisaparesr.parseArgs(arguments)
    ```

    *Note that we don't recommend the usage of the `--select` option in a python script if it's not designed to be used in a terminal, as using this option will require user input to parse files.*
