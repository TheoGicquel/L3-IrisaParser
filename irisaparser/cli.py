# -*- coding: utf-8 -*-

from operator import contains
import sys
import re
import os
import traceback
from .title_lib import *
from .authors_lib import *
from .abstract_lib import *
from .references_lib import *
from .intro_lib import *
from .body_lib import *
from .conclusion_discussion_lib import *
import pdfplumber
from tika import parser as tikaParser
import xml.dom.minidom
# @authors : L.A and K.O

# custom Exception for the sake of best practises
class ArgumentException(Exception):
    pass

# custom Exception to handle quit command from user
class QuitException(Exception):
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

def select_files(files):
    indexed_files = {}
    files_to_parse = {}

    for index,file in enumerate(files):
        indexed_files[index] = file
        print("["+str(index)+"] "+os.path.basename(file))

    def print_selected_files():
        print("\nCurrent selected files:\n")
        for index in files_to_parse:
            print("["+str(index)+"] "+os.path.basename(files_to_parse.get(index)))

    def include_file(index):
        if contains(indexed_files,index):
            file = indexed_files.get(index)
            files_to_parse[index] = file
            print("["+str(index)+"] "+os.path.basename(file)+" was added to the files to parse")
        else: print("["+str(index)+"] file is not indexed and can't be included")

    def exclude_file(index):
        if contains(files_to_parse,index):
            file = files_to_parse.pop(index)
            print("["+str(index)+"] "+os.path.basename(file)+" was removed from files to parse")
        else: print("["+str(index)+"] file is not selected and can't be exclude")

    print_select_help()

    mode = None

    choice = False
    first_regex = r"^((?P<exclude>e|exclude)|(?P<include>i|include)|(?P<cancel>c|cancel))$"

    while not choice:
        user_input = input().strip()
        match  = re.match(first_regex,user_input)
        if match:
            if match.group('exclude'):
                mode = 'exclude'
                files_to_parse = indexed_files.copy()
                print("exclude mode selected, all files are selected at start")
                choice = True

            elif match.group('include'):
                mode = 'include'
                print("include mode selected, no files selected at start")
                choice = True

            elif match.group('cancel'):
                raise QuitException()

        else:
            print("please specify a mode to start with : type 'e' or 'exclude', 'i' or 'include' or quit using 'c' or 'cancel' before selecting files.\n")


    valid = False
    general_regex = r"^((?P<exclude>e|exclude)|(?P<include>i|include)|(?P<number>[0-9]+)|(?P<interval>[0-9]+-[0-9]+)|(?P<yes>y|yes)|(?P<cancel>c|cancel)|(?P<help>h|help))$"

    while not valid:
        user_input = input().strip()
        match  = re.match(general_regex,user_input)
        if match:
            if match.group('exclude'):
                mode = 'exclude'
                print("switched to exclude mode")

            elif match.group('include'):
                mode = 'include'
                print("switched to include mode")

            elif match.group('number'):
                index = int(user_input)
                if mode == 'exclude':
                    exclude_file(index)
                else: # mode is include
                    include_file(index)
                    
                print_selected_files()

            elif match.group('interval'):
                boundary = user_input.split('-')
                first_index = int(boundary[0])
                last_index = int(boundary[1])
                if last_index < first_index:
                    print(""+user_input+" is not valid, last index must be superior or equal to the first index")
                else:
                    for step in range(((last_index-first_index)+1)):
                        if mode == 'exclude': exclude_file(first_index+step)
                        else: include_file(first_index+step)

                print_selected_files()

            elif match.group('yes'):
                valid = True

            elif match.group('cancel'):
                raise QuitException()

            elif match.group('help'):
                print_select_help()

        else:
            print("unknown input: "+user_input+" type 'h' or 'help' for help, type 'c' or 'cancel' to quit.\n")

    return files_to_parse.values()

def print_select_help():
    print("\nPlease select files to be parsed: \n\n\
    type 'e' or 'exclude' to use exclude mode, where selected files will be removed from the list.\n\
    type 'i' or 'include' to use include mode, where only selected files will be parsed.\n\
    you can switch from one mode to another, selected item will remains, allowing you to reinclude excluded files\n\n\
    type a number to include/exclude corresponding file,\n\
    type <number>'-'<number> to include/exclude multiple files at once (inclusive).\n\n\
    type 'y' or 'yes' to confirm your selection and start parsing task\n\
    type 'c' or 'cancel' to cancel the parsing and quit the program\n\n\
    type 'h' or 'help' to show this help again\n\n")


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
            print("\n\
    Usage : irisaParser.py [-h| --help] | [-d|--directory <directory> ] [-o|--ouput_directory <outputDirectory>] [-t|--text] [-x|--xml] [-s|--select] <file> [files]...\n\n\
    Options :\n\n\
    -h, --help : display this help page\n\
    -d, --directory <directory> : specify a directory whose files will be parsed, may be passed multiple times\n\
    -o, --output_directory <output directory> : specify a directory where place output files, you should not specify multiples output directories\n\
    -t, --text : specify output as text files (default unless xml is specified)\n\
    -x, --xml : specify output as xml files\n\
    -s, --select : specify that not all files should be parsed, allowing you to select which files should be parsed\n")
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
        elif current_arg == "-s" or current_arg == "--select":
            ret["select"] = True

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
    return get_title(pdf)

def extractAuthors(pdf:pdfplumber.PDF):
    return getAuthorsInfos(pdf)

def extractAbstract(tikaInput):
    extracted_abstract = abstract_extractor(tikaInput)
    return (extracted_abstract if extracted_abstract != "error" else "not found")

def extractIntroduction(tikaInput):
    return intro_extractor(tikaInput)

def extractBody(tikaInput,intro):
    return body_extractor(tikaInput,intro)

def extractConclusion(tikaInput):
    extracted_conclusion = getConclusion(tikaInput)
    return (extracted_conclusion if extracted_conclusion != None else "not found")

def extractDiscussion(tikaInput):
    extracted_conclusion = getDiscussion(tikaInput)
    return (extracted_conclusion if extracted_conclusion != None else "not found")

def extractReferences(tikaInput):
    return reference_extractor(tikaInput)

def parse_file(filename):
    pdf_parsed_by_plumber = pdfplumber.open(filename)

    pdf_parsed_by_tika = tikaParser.from_file(filename)

    ret = {}
    ret["fileName"] = os.path.basename(filename)
    ret["title"] = extractTitle(pdf_parsed_by_plumber)
    ret["authors"] = extractAuthors(pdf_parsed_by_plumber)
    ret["abstract"] = extractAbstract(pdf_parsed_by_tika)
    ret["intro"] = extractIntroduction(pdf_parsed_by_tika)
    ret["body"] = extractBody(pdf_parsed_by_tika,ret["intro"])
    ret["conclusion"] = extractConclusion(pdf_parsed_by_tika)
    ret["discussion"] = extractDiscussion(pdf_parsed_by_tika)
    ret["references"] = extractReferences(pdf_parsed_by_tika)
    return ret

def create_text_output(extracted_text,outPutPath):
    """
    Use the extracted_text dict content to create a proper (organised) text representation of the extracted text
    And write it in a file named "<pdfFileName>_extracted.txt" write the file in the location provided
    by outPutPath
    """

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
    output_text += "introduction: \n"+extracted_text["intro"]+"\n\n"
    output_text += "corps: \n"+extracted_text["body"]+"\n\n"
    output_text += "conlusion: \n"+extracted_text["conclusion"]+"\n\n"
    output_text += "discussion: \n"+extracted_text["discussion"]+"\n\n"
    output_text += "references\n"

    for ref in extracted_text["references"]:
        output_text += "\n"+ref+"\n"

    #output_text = (xml.dom.minidom.parseString(output_text)).toprettyxml()

    outFileName = extracted_text["fileName"] +".txt"#+"_extracted.txt"
    outFile = open((os.path.join(outPutPath,outFileName)),"w", encoding="utf-8")
    outFile.write(output_text)
    outFile.close()

def clean_text_for_xml(text):
    """
    replace problematic characters such as & , < , > , ' , "
    and some others by their xml entity
    """

    ret = text.replace("&","&#38;")
    ret = ret.replace("<","&#60;")
    ret = ret.replace(">","&#62;")
    ret = ret.replace("'","&#39;")
    ret = ret.replace("\"","&#34;")
    return ret

def get_xml_node(tagname,content,clean=False):
    """
    insert the content string between an xml tag using tagname.
    if clean is passed as True: use clean_text_for_xml to clean content
    """
    if clean: content = clean_text_for_xml(content)
    return "<"+tagname+">"+(str(content))+"</"+tagname+">"

def create_xml_output(extracted_text,outPutPath):
    """
    Use the extracted_text dict content to create an xml representation of the extracted text
    And write it in a file named "<pdfFileName>_extracted.xml" write the file in the location provided
    by outPutPath
    """

    output_text = get_xml_node("preamble",extracted_text["fileName"],True)
    output_text += get_xml_node("titre",extracted_text["title"],True)

    authors_text = ""

    for author in extracted_text["authors"]:
        mail_list = extracted_text["authors"][author]
        mail_text = ""
        if len(mail_list) > 0:
            if mail_list[0].strip() == "":
                mail_text = get_xml_node("mail","not found",True)
            else:
                mail_text = get_xml_node("mail",mail_list[0],True)
        else:
            mail_text = get_xml_node("mail","not found",True)
        name_text = get_xml_node("name",author,True)
        affiliation_text = get_xml_node("affiliation","not found",True)
        authors_text += get_xml_node("auteur",name_text+mail_text+affiliation_text)

    output_text += get_xml_node("auteurs",authors_text)
    output_text += get_xml_node("abstract",extracted_text["abstract"],True)
    output_text += get_xml_node("introduction",extracted_text["intro"],True)
    output_text += get_xml_node("body",extracted_text["body"],True)
    output_text += get_xml_node("discussion",extracted_text["discussion"],True)
    output_text += get_xml_node("conclusion",extracted_text["conclusion"],True)

    refs_text = ""

    for ref in extracted_text["references"]:
        refs_text+= "\n"+ref #get_xml_node("reference",ref,True)

    output_text += get_xml_node("biblio",refs_text,True)

    output_text = get_xml_node("article",output_text)
    output_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"+output_text

    try:
        output_text = (xml.dom.minidom.parseString(output_text)).toprettyxml()
    except Exception as ex:
        print(" unexpected xml error for file"+extracted_text["fileName"]+": ",end="")
        print(traceback.format_exc())
        #print(output_text)

    outFileName = extracted_text["fileName"] +".xml" #+"_extracted.xml"
    outFile = open((os.path.join(outPutPath,outFileName)),"w", encoding="utf-8")
    outFile.write(output_text)
    outFile.close()

# list of availables options
availables_option = ["-h","-d","-o","--help","--directory","--output_directory","-t","--text","-x","--xml","-s","--select"] 

# execute program with the given args , used in __init__ and __main__
def execute(args):
    try:
        ret = check_args_and_retrive_filenames(args)
        if ret.get("help") == None :
            outputDir = ret["output"] if ret.get("output") != None else "./";
            files = ret["files"]
            if ret.get("select") :
                files = select_files(files)

            for file in files:
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
    
    except QuitException as ex:
        print("exit program")