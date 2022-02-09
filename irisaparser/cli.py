import sys
import os

# TODO thinking about refactoring using dictionary instead of Array
# to nest function to str and avoid if/elif in checkArg

# return an array of file in a directory
def getFilesFromDirectories(directories):
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
def checkArg(args):

    ret = {}
    index = 0

    directories = []
    files = []
    while(index < len(args)):
        currentArg = args[index]

        # check if current arg is an option
        if(small_option.count(currentArg) > 0 or long_option.count(currentArg) > 0):
            try:
                optionIndex = small_option.index(currentArg)
            except ValueError:
                try:
                    optionIndex = long_option.index(currentArg)
                except ValueError:
                    pass

            if(optionIndex == 0): #help
                ret["help"] = True
                print("usage : irisaParser.py [-h| --help] | [-d|--directory <directory> ] [-o|--ouput_directory <outputDirectory>] <file> [files]... \n")
                print("Options : \n")
                print("-h, --help : display this help page\n")
                print("-d, --directory <directory> : specify a directory whose files will be to parsed, may be passed multiple times\n")
                print("-o, --ouput_directory <output directory> : specify a directory where place ouput files \n")
                break

            elif(optionIndex == 1): #directory

                if(index+1 >= len(args)):
                    ret["error"] = "argument missing after "+currentArg
                    break
                elif(small_option.count(args[index+1]) > 0 or long_option.count(args[index+1]) > 0):
                    ret["error"] = "invalid option "+args[index+1]+" after "+currentArg+", argument expected"
                    break
                else:
                    index += 1
                    directories.append(args[index])

            elif(optionIndex == 2): #output directory

                if(index+1 >= len(args)):
                    ret["error"] = "argument missing after "+currentArg
                    break
                elif(small_option.count(args[index+1]) > 0 or long_option.count(args[index+1]) > 0):
                    ret["error"] = "invalid option "+args[index+1]+" after "+currentArg+", argument expected"
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
            files.append(currentArg)

        index += 1

    if(ret.get("error") == None):

        for file in files:

            if(not os.path.exists(file)):
                print("file: "+file+" not found, ignored")
                files.remove(file)
            elif(not os.path.isfile(file)):
                print("file: "+file+" not a file, ignored")
                files.remove(file)

        files = files + getFilesFromDirectories(directories)

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
checkResult = checkArg(args)

if(checkResult.get("error") != None):
    print("error: "+checkResult.get("error")+"\n")
    print("use -h or --help for usage"+"\n")

elif(checkResult.get("help") == None):
    if(checkResult.get("output") != None):
        print("output: ")
        print(checkResult.get("output"))
    print("files: ")
    print(checkResult.get("files"))