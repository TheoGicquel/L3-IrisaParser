
### Example 2

**Parse multiples files in multiples directories in a specified output directory**

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
