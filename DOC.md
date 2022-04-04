# Irisa Parser Documentation

This document describe all the avaiblables options for the python module `irisaparser`.

## Command line usage

The default usage using a command is :

```sh
python3 -m irisaparser <file> [file...]
```

Without options a command argument is interpreted as a filename. But the module allow you tu use multiples options to specify the behavior of the program.

Some option just change the behavior of the program and don't need another argument such as :

- **`-h`** or **`--help`** : display the help, if this option is passed, help will be displayed and no other action will be effectued
- **`-t`** or **`--text`** : specify the output files format as text (default if `--xml` not specified), may be used allong with `--xml` for both format. 
- **`-x`** or **`--xml`** : specify the output files format as xml, may be used allong with `--text` for both format. 
- **`-s`** or **`--select`** : allow you to select which files you want to parse finnaly, after retrieving all files you passed as arguments or using the `--directory` option, this option will allow you to select which files should be extracted at the end, for more information see the **selection** section below.

*Note that no option can be aggregated, unlike many command line interface we don't allow that for exemple : `-tsx` is not a valid option syntax and will be interpreted as a filename.*

Some other need a second argument to be defined such as :

- **`-d`** or **`--directory`** `<directorypath>` : this option allow you to specify a directory where **all** files will be parsed. This option can be used multiple times to add multiples directories to the selection. Unless you use the option `--select` to filter which files you really want to parse.

- **`-o`** or **`--output-directory`** `<directorypath>` : this option allow you to specify a directory where the created files will be placed, without this option the program will place these files in the current directory. **This option cannot be specified multiples times

Note that any of these options can be passed at any order in the command argument list. Just be aware that any non-option argument will be interpreted as a filename and that options that need a second argument will use the next passed argument. Non providing an argument after one of these options will cause the program to exit.

### About the selection.

Using the `--select` option, you will have the possibility of filter which files to finnaly parse, in the list you passed to the program using plain arguments or `--directory` option. All of these files will be placed in a numbered list, that you will be abble to filter using these numbers.

For exemple using this command :

```
python3 -m irisapser fileA fileB fileC --select
```


## Python script usage

The `irisaparesr` module when imported in a python script using `import` keyword, will expose these functions :

- **`parseFile`** *(`filename, [outputDir, text, xml]`)* : which parse the specfied file.
    - `filename` : relative name of the file to parse as a `string`.
    - `ouputDir` (optional) : relative path where place extracted files as a `string`. Default is current directory.
    - `text` (optional) : indicate if the file to parse will be extracted as a text file. Used as a boolean. Default is `True`.
    - `xml` (optional) : indicate if the file to parse will be extracted as a xml file. Used as boolean. Default is False.

*Note that if both `text` and `xml` are passed as `False`, the file will be parsed but no output file will be writed.*

- **`parseFiles`** *(`files, [outputDir, text, xml]`)* : which parse specfied files, using `parseFile` function
.
    - `files` : A list (or an equivalent `iterable`) of `string` which are names of the files to parse.
    - `ouputDir` (optional) : relative path where place extracted files as a `string`. Default is current directory.
    - `text` (optional) : indicate if the file to parse will be extrextractedaced as a text file. Used as a boolean. Default is `True`.
    - `xml` (optional) : indicate if the file to parse will be extracted as a xml file. Used as boolean. Default is False.

*Note that if both `text` and `xml` are passed as `False`, files will be parsed but no output file will be writed.* 

- **`parseArgs`** *(`args`)* : allow you to use the module in a script with all the options of the command line.
    - `args` : a list (or an equivalent `iterable`) of `string` which are arguments, to know more about arguments and avaiblables options check the **Command line usage** section above.

## Exemples