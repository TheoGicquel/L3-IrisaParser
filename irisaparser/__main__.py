import traceback
import pdfplumber
from .cli import *

try:
    ret = check_args_and_retrive_filenames(sys.argv[1:])
    if ret.get("help") == None :
        outputDir = ret["output"] if ret.get("output") != None else "./";
        for file in ret["files"]:
            try:
                extracted_text = parse_file(file)
                if ret["text"]: create_text_output(extracted_text,outputDir)
                if ret["xml"]: create_xml_output(extracted_text,outputDir)
            except pdfplumber.pdfminer.pdfparser.PDFSyntaxError as ex:
                print("file: "+file+" is probably not a pdf, ignored")
            except UnicodeEncodeError as ex:
                print(" unexpected unicode error: ",end="")
                print(traceback.format_exc())

except ArgumentException as ex:
    print("error: "+str(ex))
    print("use -h or --help for usage"+"\n")