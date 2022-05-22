
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
