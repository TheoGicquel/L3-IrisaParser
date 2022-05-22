## Module usage

The `irisaparser` module when imported into a python script using the `import` keyword, will expose the following methods :

- **`parseFile`** *(`filepath, [outputDir, text, xml]`)* : Parses a single specific file.
  - `filepath` : (`string`) Relative path of the file to parse.
  - `ouputDir` (`string`) (optional) : relative path of output directory location. Set to current directory by default.
  - `text` (`Boolean`)(optional) : specifies if parsed file output should be written into a plain text file. Set to `True` by default.
  - `xml` (`Boolean`)(optional) : specifies if the parsed file output should be written and formatted into an XML file. set to `False` by default.

*Please note that if both `text` and `xml` are set to `False`, the file will be parsed but no output file will be created.*

- **`parseFiles`** *(`files, [outputDir, text, xml]`)* : Parses specified files, using `parseFile` function
.
  - `files` : (`Iterable`) A list (or an equivalent `iterable`) of `string` of paths of files to parse.
- `ouputDir` (`String`) (optional) : relative path of output directory location. Set to current directory by default.
  - `text` (`Boolean`) (optional) : specifies if parsed file output should be written into a plain text file. Set to `True` by default.
  - `xml` (`Boolean`) (optional) : specifies if the parsed file output should be written and formatted into an XML file. set to `False` by default.
*Please note that if both `text` and `xml` are set to `False`, files will be parsed but no output file will be created.*

- **`parseArgs`** *(`args`)* : allows you to use the module in a script with all command line options.
  - `args` : a list (or an equivalent `iterable`) of `string` which are arguments, to know more about arguments and available options check the **Command line usage** section above.
