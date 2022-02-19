#!/usr/bin/env python
# coding: utf-8
# @author O.K

import json
import glob
import difflib
import pdfplumber
import spacy
import re
import time
from datetime import timedelta

nlp = spacy.load("en_core_web_md")


def getExpectedInfoOnPDF(pdfFilePath):
    # Datas are in JSON file in the same folder BUT with different name ( SPECIFIC TO ISTEX CORPUS )
    with open(glob.glob(pdfFilePath.split("/")[0]+"/*.json")[0]) as jsonFile: 
        return json.load(jsonFile)



def getAuthors(pdfFilePathTitle,pageNumber=0):
    
    pdfData = pdfplumber.open(pdfFilePathTitle)

    if pageNumber==0:
        
        # Some chars are exponent near the name so we have to delete them in order to have correct names
        meanFontSize = 0
        numberOfChars = 0        
        
        # Calculate mean of font size in the page
        for char in pdfData.pages[pageNumber].chars:
            meanFontSize += char["size"]
            numberOfChars+=1

        # Remove exponent chars
        for char in pdfData.pages[pageNumber].chars:
            if char["size"]<(meanFontSize/numberOfChars)-1:
                char["text"]=""

            
    # Get 1200 first words on the first page
    currentPageText = pdfData.pages[pageNumber].extract_text(x_tolerance=1.8,y_tolerance=2)[:800]
    
    # Remove unecessary chars in text extracted
    currentPageText = re.sub(" +"," ",currentPageText)
    currentPageText = re.sub("[0-9]","",currentPageText)
    currentPageText = re.sub("\(","",currentPageText)
    currentPageText = re.sub("\)","",currentPageText)
    currentPageText = re.sub("a´","a",currentPageText)
    currentPageText = re.sub("&\n","and ",currentPageText)
    currentPageText = re.sub("´e","é",currentPageText)
    currentPageText = re.sub("e´","é",currentPageText)
    currentPageText = re.sub("c¸","ç",currentPageText)
    currentPageText = re.sub("ˆı","î",currentPageText)
    
    
  
        
    doc = nlp(currentPageText)
    namesFound = []
    
    # Because names are generally stacked, if we found a name not in the fisrt stack of the name we ignore it
    lastNamePosition = 0
    
    for ent in doc.ents:
        if ent.label_ == "PERSON" and (ent.start_char - lastNamePosition <= 60 or lastNamePosition==0):
            lastNamePosition=ent.start_char
            namesFound.append(ent.text.strip().lower())
    
    # In some PDF, the first page is a cover page so we have to check the next page
    if not namesFound and pageNumber==0:
        return getAuthors(pdfFilePathTitle,1) # Recursive call

    return namesFound

def getPercentageSimilitudeAuthors(expectedAuthors,extractedAuthors):    
    expectedAuthors = [a for b in expectedAuthors for a in b.split()]
    extractedAuthors = [a for b in extractedAuthors for a in b.split()]
    return difflib.SequenceMatcher(None,expectedAuthors,extractedAuthors).ratio()*100



def getTitle(pdfFilePath):
    # TODO @Theo put here your code
    return "Fake Title"

def getPercentageSimilitudeTitle(expectedTitle,extractedTitle):
    return difflib.SequenceMatcher(None,expectedTitle.split(),extractedTitle.split()).ratio()*100 # Split to compare word by word



def getAbstract(pdfFilePathTitle):
    # TODO @Corentin / @CertesCertes put here your code    
    return "Fake Abstract"

def getPercentageSimilitudeAbstract(expectedAbstract,extractedAbstract):
    return difflib.SequenceMatcher(None,expectedAbstract.split(),extractedAbstract.split()).ratio()*100 # Split to compare word by word



# Variables to store the precision on all PDFs
globalPrecisionTitle = 0.
globalPrecisionAuthors = 0.
globalPrecisionAbstract = 0.

# Number of PDFs treated
numberOfPDFfiles = 0

# Benchmark time
start_time = time.time()

# For each PDF file in the current and subsequent directory
for pdfFile in glob.glob('**/*.pdf'):
    
    """
    # Just treat 100 PDFs to tests some changes
    if numberOfPDFfiles==100:
        break
    """
    
    # Get expected data (title, authors, abstract, etc ....)
    data = getExpectedInfoOnPDF(pdfFile) 
    
    # In some case, the JSON file doesn't have informations we needed
    if not all (key in data.keys() for key in ("title","author","abstract")):
        continue # Go to the next pdf 
    
    # Calculate the precision between the extraction we made and the expected value
    precisionTitle = getPercentageSimilitudeTitle(data["title"],getTitle(pdfFile))
    precisionAuthors = getPercentageSimilitudeAuthors([author["name"].lower() for author in data["author"]], getAuthors(pdfFile))
    precisionAbstract = getPercentageSimilitudeAbstract(data["abstract"],getAbstract(pdfFile))
    
    
    print("[+] "+ pdfFile)
    print("\t Title : " + str(precisionTitle) +" %")
    print("\t Authors : "+ str(precisionAuthors) +" %")    
    print("\t Abstract : "+ str(precisionAbstract) +" %\n")
    
    # Add this precision to the global precision
    globalPrecisionTitle+=precisionTitle
    globalPrecisionAuthors+=precisionAuthors
    globalPrecisionAbstract+=precisionAbstract
    
    numberOfPDFfiles+=1
    
if numberOfPDFfiles>0:    
    print("-"*60)
    print("\n[+] Total (on " + str(numberOfPDFfiles) + " files in " + str(timedelta(seconds=(time.time() - start_time))) + ") :")
    print("\t Title : " + str(globalPrecisionTitle / numberOfPDFfiles) + " %")
    print("\t Authors : " + str(globalPrecisionAuthors / numberOfPDFfiles) + " %")
    print("\t Abstract : " + str(globalPrecisionAbstract / numberOfPDFfiles) + " %\n")
    print("-"*60)
