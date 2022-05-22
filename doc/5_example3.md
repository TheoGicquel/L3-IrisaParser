
### Example 3

*Note that to use the module in a script you need to build and install it using a build utility, how to build this module as a python package is explained in the [README](https://gitlab.com/inf1603/irisaparser/-/blob/master/README.md) (The `README.md` file in the source).*

- **Parse a file using a python script**

    *The full documentation fo these functions is explained in the **Python script usage** section above*

    To do this we use the `parseFile` method exposed by the module, here is a simple script to parse a file named `somepdf.pdf` located in `/tmp` using both output type, txt and XML:

    ```py
    import irisaparser # import the module

    irisaparesr.parseFile('/tmp.somepdf.pdf',xml=True);
    # note that txt is passed as True by default
    ```

- **Parse multiples files using a python script**

    For this you could use any iterable structure of strings and pass it to the function `parseFile` however we will create a little utility to recursively parse all files ending with the `.pdf` extension from a directory given as argument:

    ```py
    import irisaparser # as usual
    import os.path # to manipulate filenames and directories

    main_directory = sys.arg[1] # the first argument passed

    files = [] # list of selected files

    def select_files_from_directory(directory): # function to call for recursivly
        if os.path.isdir(directory): # to be sure that a directory was passed
            for file in os.listdir(directory):

                if os.isdir(file):
                    select_files_from_directory(file) # if we encounter the directory we call the function once more
                elif os.path.splitext(file)[1] == '.pdf':
                    files.append(file)

    select_files_from_directory(main_directory) # first call to the recursive function

    if files.count > 0: # do not parse empty list
        irisaparser.parseFiles(files) # place output txt files in current directory
    ```

    *There are multiple ways in python to go recursively through directories, whe chose this one because it was simpler to explain*

- **Pass multiples options to the program using a python script**

    This function allows you to use the module like a command line utility inside a python script, this works in the same way as the command line, just pass a `list` (or any `iterable`) of arguments as `string`, here is a simple example:

    Here we parse the file `somefile.pdf` from our current directory and place the xml output in the `/tmp` directory.

    ```py
    import irisaparser; # as needed

    arguments = ['./somefile.pdf','-o','/tmp','-x'] # arguments list

    irisaparesr.parseArgs(arguments)
    ```

    *Note that we don't recommend the usage of the `--select` option in a python script if it's not designed to be used in a terminal, as using this option will require user input to parse files.*
