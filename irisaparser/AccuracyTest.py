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
import multiprocessing
import os

from pathlib import Path
nlp = spacy.load(Path('CustomNER/'))


def getExpectedInfoOnPDF(pdfFilePath):
    # Datas are in JSON file in the same folder BUT with different name
    with open(glob.glob("/".join(pdfFilePath.split("/")[:-1])+"/*.json")[0]) as jsonFile: 
        return json.load(jsonFile)


def getAuthors(pdfFilePathTitle,pageNumber=0):
    
    pdfData = pdfplumber.open(pdfFilePathTitle)
    #print(pdfData.metadata)
    if pageNumber==0:
        
        # Some chars are exponent near the name so we have to delete them in order to have correct names
        meanFontSize = 0
        numberOfChars = 0        
        
        # Calculate mean of font size in the page
        try:
            for char in pdfData.pages[pageNumber].chars:
                meanFontSize += char["size"]
                numberOfChars+=1
        except TypeError:
            print("ERR : ",pdfFilePathTitle)
            return []
        except ValueError:
            print("ERR : ",pdfFilePathTitle)
            return []  
            
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
        if ent.label_ == "JPP" and (ent.start_char - lastNamePosition <= 60 or lastNamePosition==0):
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



def treatPDF(pdfFile):
    
    #Need to tell this function to use global variables
    global globalPrecisionTitle
    global globalPrecisionAuthors
    global globalPrecisionAbstract
    global numberOfPDFfiles
    
    # Get expected data (title, authors, abstract, etc ....)
    data = getExpectedInfoOnPDF(pdfFile) 
    
    # In some case, the JSON file doesn't have informations we needed
    if not all (key in data.keys() for key in ("title","author","abstract")):
        return # Go to the next pdf 
    
    # Calculate the precision between the extraction we made and the expected value
    precisionTitle = getPercentageSimilitudeTitle(data["title"],getTitle(pdfFile))
    precisionAuthors = getPercentageSimilitudeAuthors([author["name"].lower() for author in data["author"]], getAuthors(pdfFile))
    precisionAbstract = getPercentageSimilitudeAbstract(data["abstract"],getAbstract(pdfFile))
    
    """
    print("[+] "+ pdfFile)
    print("\t Title : " + str(precisionTitle) +" %")
    print("\t Authors : "+ str(precisionAuthors) +" %")    
    print("\t Abstract : "+ str(precisionAbstract) +" %\n")
    """

    # Add this precision to the global precision
    globalPrecisionTitle.value+=precisionTitle
    globalPrecisionAuthors.value+=precisionAuthors
    globalPrecisionAbstract.value+=precisionAbstract
    
    numberOfPDFfiles.value+=1


# Variables to store the precision on all PDFs.
# Using some IPC(Inter-Process Communication) in order 
# to share the variable in the different processes that will be created 
globalPrecisionTitle = multiprocessing.Value("d",0)
globalPrecisionAuthors = multiprocessing.Value("d",0)
globalPrecisionAbstract = multiprocessing.Value("d",0)

# Number of PDFs treated 
numberOfPDFfiles = multiprocessing.Value("i",0)

# Benchmark time
start_time= time.time()

# Get all PDFs path
allPDFs = glob.glob('ISTEX_Corpus/**/*.pdf')

# Prepare a pool of cpu_count() process
pool = multiprocessing.Pool(multiprocessing.cpu_count())


for pdfFile in allPDFs:
    pool.apply_async(func=treatPDF, args=(pdfFile,)) # Adds the task to the queue. It will be processed when 1 of the cpu_count() processes in the pool is available

pool.close() # No more task to entry in the pool
pool.join() # Before continuing, wait until all tasks are completed

if numberOfPDFfiles.value>0:    
    print("-"*60)
    print("\n[+] Total (on " + str(numberOfPDFfiles.value) + " files in " + str(timedelta(seconds=(time.time() - start_time))) + ") :")
    print("\t Title : " + str(globalPrecisionTitle.value / numberOfPDFfiles.value) + " %")
    print("\t Authors : " + str(globalPrecisionAuthors.value / numberOfPDFfiles.value) + " %")
    print("\t Abstract : " + str(globalPrecisionAbstract.value / numberOfPDFfiles.value) + " %\n")
    print("-"*60)
