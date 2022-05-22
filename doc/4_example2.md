
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
