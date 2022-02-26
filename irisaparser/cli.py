import sys
import os

# @authors : L.A and K.O

# custom Exception for the sake of best practises
class ArgumentException(Exception):
    pass

# return an array of file in a list of directories (not recursively)
def get_files_from_directories(files,directories):
    newFiles = []

    for directory in directories:
        if(os.path.exists(directory)):
            if(os.path.isdir(directory)):
                dirFiles = os.listdir(directory)
                for fileName in dirFiles:
                    file = os.path.join(directory,fileName)
                    if(os.path.isfile(file)):
                        if not file in files:
                            newFiles.append(file)
                        else:
                            print("file: "+file+" in directory: "+directory+" already provided, ignored")
            else:
                print("directory: "+directory+" not a directory, ignored")
        else:
            print("directory: "+directory+" not found, ignored")

        if(len(newFiles) == 0): print("directory: "+directory+" no valid file found")

    return newFiles


def check_args_and_retrive_filenames(args):
    """
    check arguments and return a dict
    where key represents result of argument parsing posible keys :

    - "help" -> if help key is set then help message was displayed and nothing else should be done
    - "output" -> if output key is set then an output dir was specified, the value of the key is the path of the output directory
    - "files" -> this key is always set except when help key is set

    raise ArgumentException if an illegal argument combination is passed,
    note that missing files and directory are ignored and don't raise exception
    """

    argsCount = len(args)

    index = 0

    directories = []
    files = []

    ret = {}

    while(index < argsCount):
        current_arg = args[index]

        if current_arg == "-h" or current_arg == "--help": #help
            ret = {}
            ret["help"] = True
            print("usage : irisaParser.py [-h| --help] | [-d|--directory <directory> ] [-o|--ouput_directory <outputDirectory>] <file> [files]...\n \
            Options :\n \
            -h, --help : display this help page\n \
            -d, --directory <directory> : specify a directory whose files will be to parsed, may be passed multiple times\n \
            -o, --ouput_directory <output directory> : specify a directory where place output files, you should not specify multiples output directories")
            return ret

        elif current_arg == "-d" or current_arg == "--directory": #directory

            if(index+1 >= len(args)):
                raise ArgumentException("argument missing after "+current_arg)
            elif(args[index+1] in availables_option):
                raise ArgumentException("invalid option "+args[index+1]+" after "+current_arg+", directory expected")
            else:
                index += 1
                directories.append(args[index])

        elif current_arg == "-o" or current_arg == "--output_directory": #output directory

            if(ret.get("output") != None):
                raise ArgumentException("invalid duplicated option "+current_arg+", multiple output directories not allowed")
            if(index+1 >= len(args)):
                raise ArgumentException("argument missing after "+current_arg)
            elif(args[index+1] in availables_option):
                raise ArgumentException("invalid option "+args[index+1]+" after "+current_arg+", argument expected")
            else:
                index += 1
                outputDir = args[index]

                if(not os.path.exists(outputDir)):
                    raise ArgumentException("provided output "+outputDir+" not found")
                elif(not os.path.isdir(outputDir)):
                    raise ArgumentException("provided output "+outputDir+" is not a directory")
                else:
                    ret["output"] = outputDir

        # if not an option then it must be a file
        elif(not current_arg in files):
            files.append(current_arg)
        else:
            print("file: "+current_arg+" already provided, ignored")
        index += 1

    for file in files:

        if(not os.path.exists(file)):
            print("file: "+file+" not found, ignored")
            files.remove(file)
        elif(not os.path.isfile(file)):
            print("file: "+file+" not a file, ignored")
            files.remove(file)

    if(len(directories) > 0):
        files = files + get_files_from_directories(files,directories)

    if(len(files) < 1):
        raise ArgumentException("no valid file provided")

    ret["files"] = files

    return ret


def extractFileName(input):
    # TODO
    pass

def extractTitle(input):
    # TODO
    pass

def extractAuthors(input):
    # TODO
    pass

def extractAbstract(input):
    # TODO
    pass

def parse_file(filename):

    # TODO pdf work here

    # TODO input for extracts here

    ret = {}
    ret["fileName"] = extractFileName(None)
    ret["title"] = extractTitle(None)
    ret["authors"] = extractAuthors(None)
    ret["abstract"] = extractAbstract(None)
    return ret

def create_text_output(extracted_text,outPutPath):

    authorsStr = "auteurs: "

    if len(extracted_text["authors"]) > 1 :
        authorsStr += "\n"
        for author in extracted_text["authors"]:
            authorsStr += author+"\n"
    else:
        authorsStr += extracted_text["authors"][0]+"\n"

    output_text = "fichier source: "+extracted_text["fileName"]+"\n\n"
    output_text += "titre: "+extracted_text["titre"]+"\n\n"
    output_text += authorsStr+"\n"
    output_text += "abstract: \n"+extracted_text["abstract"]+"\n"

    outFileName = extracted_text["fileName"]+"_extracted.txt"
    outFile = open((os.path.join(outPutPath,outFileName)),"wt")
    outFile.write(output_text)
    outFile.close()

# list of availables options
availables_option = ["-h","-d","-o","--help","--directory","--output_directory"] 

if __name__ == "__main__":
    try:
        ret = check_args_and_retrive_filenames(sys.argv[1:])
        if ret.get("help") == None :
            print(str(ret["files"])) # debug
            # TODO uncomment that when merging stuff
            #outputDir = ret["output"] if ret.get("ouput") != None else "./";
            #for file in ret["files"]:
            #    extracted_text = parse_file(file)
            #    create_text_output(extracted_text,outputDir)
    except ArgumentException as ex:
        print("error: "+str(ex))
        print("use -h or --help for usage"+"\n")