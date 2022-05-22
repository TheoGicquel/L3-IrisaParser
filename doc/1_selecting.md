
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
