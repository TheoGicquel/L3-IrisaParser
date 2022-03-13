import traceback
import pdfplumber
from .cli import *

def parseFile(filename,outputDir='./'):
    extracted_data = cli.parse_file(filename)
    cli.create_text_output(extracted_data,outputDir)

def parseFiles(files,outputDIr='/'):
    for file in files:
        parseFile(file)

def parseArgs(args):
    try:
        ret = cli.check_args_and_retrive_filenames(args)
        if ret.get("help") == None :
            outputDir = ret["output"] if ret.get("output") != None else "./";
            for file in ret["files"]:
                try:
                    extracted_text = cli.parse_file(file)
                    cli.create_text_output(extracted_text,outputDir)
                except pdfplumber.pdfminer.pdfparser.PDFSyntaxError as ex:
                    print("file: "+file+" is probably not a pdf, ignored")
                except UnicodeEncodeError as ex:
                    print(" unexpected unicode error: ",end="")
                    print(traceback.format_exc())

    except cli.ArgumentException as ex:
        print("error: "+str(ex))
        print("use -h or --help for usage"+"\n")