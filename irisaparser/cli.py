import sys
import os
import traceback
from .title_lib import *
from .authors_lib import *
from .abstract_lib import *
import pdfplumber
from tika import parser as tikaParser
import xml.dom.minidom
from xml.sax.saxutils import escape
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

    text_output = False
    xml_output = False

    while(index < argsCount):
        current_arg = args[index]

        if current_arg == "-h" or current_arg == "--help": #help
            ret = {}
            ret["help"] = True
            print("usage : irisaParser.py [-h| --help] | [-d|--directory <directory> ] [-o|--ouput_directory <outputDirectory>] <file> [files]...\n \
            Options :\n \
            -h, --help : display this help page\n \
            -d, --directory <directory> : specify a directory whose files will be to parsed, may be passed multiple times\n \
            -o, --ouput_directory <output directory> : specify a directory where place output files, you should not specify multiples output directories\n \
            -t, --text : specify output as text files (default unless xml is specified)\n \
            -x, --xml : specify output as xml files")
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

        elif current_arg == "-t" or current_arg == "--text":
            text_output = True
        elif current_arg == "-x" or current_arg == "--xml":
            xml_output = True

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

    ret["text"] = text_output if xml_output else True
    ret["xml"] = xml_output

    return ret

def extractTitle(pdf:pdfplumber.PDF):
    return parse_title(pdf)

def extractAuthors(pdf:pdfplumber.PDF):
    return getAuthors(pdf)

def extractAbstract(tikaInput):
    extracted_abstract = abstract_extractor(tikaInput)
    return (extracted_abstract if extracted_abstract != "error" else "not found")

def extractReferences(tikaInput):
    return references_lib.reference_extractor(tikaInput)

def parse_file(filename):
    pdf_parsed_by_plumber = pdfplumber.open(filename)

    pdf_parsed_by_tika = tikaParser.from_file(filename)

    ret = {}
    ret["fileName"] = os.path.basename(filename)
    ret["title"] = extractTitle(pdf_parsed_by_plumber)
    ret["authors"] = extractAuthors(pdf_parsed_by_plumber)
    ret["abstract"] = extractAbstract(pdf_parsed_by_tika)
    ret["references"] = extractReferences(pdf_parsed_by_tika)
    return ret

def create_text_output(extracted_text,outPutPath):

    authorsStr = "auteurs: "
    
    for key in extracted_text["authors"]:
        mailList = extracted_text["authors"][key]
        authorsStr+="\n"+key+" ("
        if mailList != None:
            authorsStr+= ", ".join(mailList)
        else:
            authorsStr="mail not found"
        authorsStr+=")"

    if not extracted_text["authors"]:
        authorsStr+=" not found"

    output_text = "fichier source: "+extracted_text["fileName"]+"\n\n"
    output_text += "titre: "+extracted_text["title"]+"\n\n"
    output_text += authorsStr+"\n\n"
    output_text += "abstract: \n"+extracted_text["abstract"]+"\n\n"
    output_text += "references\n"

    for ref in extracted_text["references"]:
        output_text += "\n"+ref+"\n"

    #output_text = (xml.dom.minidom.parseString(output_text)).toprettyxml()

    outFileName = extracted_text["fileName"]+"_extracted.txt"
    outFile = open((os.path.join(outPutPath,outFileName)),"w", encoding="utf-8")
    outFile.write(output_text)
    outFile.close()


# TODO remove this one, xml.dom.minidom.toprettyxml used instead
def clean_text_for_xml(text):
    return text.replace("\n"," ")

def get_xml_node(tagname,content):
    return "<"+tagname+">"+(str(content))+"</"+tagname+">"

def create_xml_output(extracted_text,outPutPath):

    output_text = get_xml_node("preamble",extracted_text["fileName"])
    output_text += get_xml_node("titre",extracted_text["title"])

    authors_text = ""

    for author in extracted_text["authors"]:
        mail_list = extracted_text["authors"][author]
        mail_text = ""
        for mail in mail_list:
            mail_text += get_xml_node("mail",mail)
        mail_text = get_xml_node("mails",mail_text)
        name_text = get_xml_node("name",author)
        authors_text += get_xml_node("auteur",name_text+mail_text)

    output_text += get_xml_node("auteurs",authors_text)
    output_text += get_xml_node("abstract",extracted_text["abstract"])

    refs_text = ""

    for ref in extracted_text["references"]:
        refs_text+= get_xml_node("reference",ref)

    output_text += get_xml_node("biblio",refs_text)

    output_text = get_xml_node("article",output_text)
    output_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"+output_text

    try:
        tmp_text = output_text.replace("&","&#38;")
        output_text = (xml.dom.minidom.parseString(tmp_text)).toprettyxml()
    except Exception as ex:
        print(" unexpected xml error for file"+extracted_text["fileName"]+": ",end="")
        print(traceback.format_exc())
        #print(output_text)

    outFileName = extracted_text["fileName"]+"_extracted.xml"
    outFile = open((os.path.join(outPutPath,outFileName)),"w", encoding="utf-8")
    outFile.write(output_text)
    outFile.close()

# list of availables options
availables_option = ["-h","-d","-o","--help","--directory","--output_directory","-t","--test","-x","--xml"] 

if __name__ == "__main__":
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