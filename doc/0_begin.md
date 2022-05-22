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
