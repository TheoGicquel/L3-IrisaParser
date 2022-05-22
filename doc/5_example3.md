
### Example 3

*Note that to use the module in a script you need to build and install it using a build utility, how to build this module as a python package is explained in the [README](https://gitlab.com/inf1603/irisaparser/-/blob/master/README.md) (The `README.md` file in the source).*

- **Parse a file using a python script**

    *The full documentation fo these functions is explained in the **Python script usage** section above*

    For this we use the `parseFile` function exposed by the module, here is a simple script to parse a file named `somepdf.pdf` located in `/tmp` using both output type, txt and xml:

    ```py
    import irisaparser # import the module

    irisaparesr.parseFile('/tmp.somepdf.pdf',xml=True);
    # note that txt is passed as True by default
    ```

- **Parse multiples files using a python script**

    For this you could use any iterable structures of string and pass it to the function `parseFile` but we will make a little utility to recursively parse all files ending by the `.pdf` extension from a directory gived as argument:

    ```py
    import irisaparser # as usual
    import os.path # to manipulate filenames and directories

    main_directory = sys.arg[1] # the first argument passed

    files = [] # list of selected files

    def select_files_from_directory(directory): # function for recursivty
        if os.path.isdir(directory): # to be sure that a directory was passed
            for file in os.listdir(directory):

                if os.isdir(file):
                    select_files_from_directory(file) # if we ancounter ta directory we call the function another time
                elif os.path.splitext(file)[1] == '.pdf':
                    files.append(file)

    select_files_from_directory(main_directory) # first call to the recursive function

    if files.count > 0: # don't parse empty list
        irisaparser.parseFiles(files) # place output txt files in current directory
    ```
    *There is multiples ways in python to parcour recursively diretories, whe choose this one because it was simple to explain for us*

- **Pass multiples options to the program using a python script**

    This function allow you to use the module like a command line utility in a python script, this word just as the command line does, just pass a `list` (or any `iterable`) of arguments as `string`, here is a simple example:

    Here we parse the file `somefile.pdf` from our current directory and place the xml output in the `/tmp` directory.

    ```py
    import irisaparser; # as needed

    arguments = ['./somefile.pdf','-o','/tmp','-x'] # arguments list

    irisaparesr.parseArgs(arguments)
    ```
    
    *Note that we don't recommend the usage of the `--select` option in a python script if it's not designed to be used in a terminal, as using this option will require user input to parse files.*