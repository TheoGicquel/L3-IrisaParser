from .cli import *

def parseFile(filename,outputDir='./',text=True,xml=False):
    extracted_data = cli.parse_file(filename)
    if text: cli.create_text_output(extracted_data,outputDir)
    if xml: cli.create_xml_output(extracted_data,outputDir)

def parseFiles(files,outputDir='./',text=True,xml=False):
    for file in files:
        parseFile(file,outputDir,text,xml)

def parseArgs(args):
    cli.execute(args)