
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
