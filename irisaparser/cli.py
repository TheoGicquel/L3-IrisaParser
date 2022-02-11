import sys
import os

# TODO thinking about refactoring using dictionary instead of Array
# to nest function to str and avoid if/elif in check_args

# return an array of file in a directory
def get_files_from_directories(directories):
    files = []

    for directory in directories:
        if(os.path.exists(directory)):
            if(os.path.isdir(directory)):
                dirFiles = os.listdir(directory)
                for fileName in dirFiles:
                    file = os.path.join(directory,fileName)
                    if(os.path.isfile(file)):
                        files.append(file)
            else:
                print("directory: "+directory+" not a directory, ignored")
        else:
            print("directory: "+directory+" not found, ignored")

        if(len(files) == 0): print("directory: "+directory+" no valid file found")

    return files

# check args
def check_args(args):

    ret = {}
    index = 0

    directories = []
    files = []
    while(index < len(args)):
        current_arg = args[index]

        # check if current arg is an option
        if(small_option.count(current_arg) > 0 or long_option.count(current_arg) > 0):
            try:
                option_index = small_option.index(current_arg)
            except ValueError:
                try:
                    option_index = long_option.index(current_arg)
                except ValueError:
                    pass

            if(option_index == 0): #help
                ret["help"] = True
                print("usage : irisaParser.py [-h| --help] | [-d|--directory <directory> ] [-o|--ouput_directory <outputDirectory>] <file> [files]... \n")
                print("Options : \n")
                print("-h, --help : display this help page\n")
                print("-d, --directory <directory> : specify a directory whose files will be to parsed, may be passed multiple times\n")
                print("-o, --ouput_directory <output directory> : specify a directory where place ouput files \n")
                break

            elif(option_index == 1): #directory

                if(index+1 >= len(args)):
                    ret["error"] = "argument missing after "+current_arg
                    break
                elif(small_option.count(args[index+1]) > 0 or long_option.count(args[index+1]) > 0):
                    ret["error"] = "invalid option "+args[index+1]+" after "+current_arg+", argument expected"
                    break
                else:
                    index += 1
                    directories.append(args[index])

            elif(option_index == 2): #output directory

                if(ret.get("output") != None):
                    ret["error"] = "invalid duplicated option "+current_arg+", multiple output directories not allowed"
                    break
                if(index+1 >= len(args)):
                    ret["error"] = "argument missing after "+current_arg
                    break
                elif(small_option.count(args[index+1]) > 0 or long_option.count(args[index+1]) > 0):
                    ret["error"] = "invalid option "+args[index+1]+" after "+current_arg+", argument expected"
                    break
                else:
                    index += 1
                    outputDir = args[index]

                    if(not os.path.exists(outputDir)):
                        ret["error"] = "provided output "+outputDir+" not found"
                        break
                    elif(not os.path.isdir(outputDir)):
                        ret["error"] = "provided output "+outputDir+" is not a directory"
                        break
                    else:
                        ret["output"] = outputDir

        # if not an option then it must be a file
        else:
            files.append(current_arg)

        index += 1

    if(ret.get("error") == None and ret.get("help") == None):

        for file in files:

            if(not os.path.exists(file)):
                print("file: "+file+" not found, ignored")
                files.remove(file)
            elif(not os.path.isfile(file)):
                print("file: "+file+" not a file, ignored")
                files.remove(file)

        if(len(directories) > 0):
            files = files + get_files_from_directories(directories)

        if(len(files) < 1): 
            ret["error"] = "no valid file provided"

        ret["files"] = files

    return ret

# list of availables options
small_option = ["-h","-d","-o"]
long_option = ["--help","--directory","--output_directory"]

# args (file name is removed)
args = sys.argv
args.remove(args[0])

# check args
check_result = check_args(args)

if(check_result.get("error") != None):
    print("error: "+check_result.get("error")+"\n")
    print("use -h or --help for usage"+"\n")

elif(check_result.get("help") == None):
    if(check_result.get("output") != None):
        print("output: ")
        print(check_result.get("output"))
    print("files: ")
    print(check_result.get("files"))