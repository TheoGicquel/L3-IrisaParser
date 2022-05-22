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
