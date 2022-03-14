import spacy
import glob
import json
import re
import pdfplumber
import pickle 
import time
from os.path import exists
from multiprocessing import Manager, Pool, cpu_count, Value
import random
from pathlib import Path

def getExpectedInfoOnPDF(pdfFilePath):
    # Datas are in JSON file in the same folder BUT with different name
    with open(glob.glob("/".join(pdfFilePath.split("/")[:-1])+"/*.json")[0]) as jsonFile: 
        return json.load(jsonFile)


def getText(pdfFilePathTitle):
    
    pdfData = pdfplumber.open(pdfFilePathTitle)
    # Some chars are exponent near the name so we have to delete them in order to have correct names
    meanFontSize = 0
    numberOfChars = 0        
        
    # Calculate mean of font size in the page
    try:
        for char in pdfData.pages[0].chars:
            meanFontSize += char["size"]
            numberOfChars+=1
    except TypeError:
        #print("ERR : ",pdfFilePathTitle)
        return ""
    except ValueError:
        #print("ERR : ",pdfFilePathTitle)
        return ""  
    
    # Remove exponent chars
    for char in pdfData.pages[0].chars:
        if char["size"]<(meanFontSize/numberOfChars)-1:
            char["text"]=""

            
    # Get 1200 first words on the first page
    currentPageText = pdfData.pages[0].extract_text(x_tolerance=1.8,y_tolerance=2)[:1200]
    
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
    
    
    return currentPageText        


# As we will parallelize the preprocessing of the PDFs in order to train the model, using some IPC(Inter-Process Communication) in order 
# to share the variable in the different processes that will be created 
manager = Manager()
TRAIN_DATA = manager.list()

def worker(pdfFile):
    # Need to tell this function to use global variables
    global totalUnsablePDF
    # Flag that will be used to know if some PDFs can't be used to train the model
    pdfCantBeUsed=False
    # Get expected data (title, authors, abstract, etc ....)
    data = getExpectedInfoOnPDF(pdfFile)
    # In some case, the JSON file doesn't have informations we needed
    if not all (key in data.keys() for key in ("title","author","abstract")):
        totalUnsablePDF.value+=1
        return # Go to the next pdf
    # Expected authors 
    expectedAuthors = [author["name"] for author in data["author"]]
    
    # Extract text on the PDF
    txt = getText(pdfFile)
    # For each expected authors
    for author in expectedAuthors:
        
        # If we don't find it inside the text extracted
        if txt.find(author)==-1:
            pdfCantBeUsed=True
            totalUnsablePDF.value+=1
            break
    # If the PDF can be used to train the model        
    if not pdfCantBeUsed:
        
        # Will store the positions (start and end index) of the names inside the previously extracted text, and the associated label (here PERSON)
        e={"entities":[]} 
        
        # For each expected authors
        for author in expectedAuthors:
            k = txt.find(author) # Retrieve start index of the name
            e["entities"].append((k,k+len(author),"JPP")) # Adding : start index, end index, label PERSON to the entities
        TRAIN_DATA.append((txt,e))




# If we have already prepared datasets for training the model
if exists("listTrained_1645905841.pkl"):
    with open('listTrained_1645905841.pkl', 'rb') as f:
        TRAIN_DATA = pickle.load(f)
        
else: # Else need to prepare datasets

    # Get all PDFs for training 
    allPDFs = glob.glob('CustomNERTraining/Training/**/*.pdf')

    # Number of PDFs treated 
    numberOfPDFfiles = Value("i",0)

    # Total unsable PDFs for training (use for DEBUG purpose)
    totalUnsablePDF = Value("i",0)

    # Prepare a pool of cpu_count() process
    pool = Pool(cpu_count())

    for pdfFile in allPDFs:
        numberOfPDFfiles.value+=1
        pool.apply_async(func=worker, args=(pdfFile,))

    pool.close() # No more task to entry in the pool
    pool.join() # Before continuing, wait until all tasks are completed

    # Will save on the disk the training datasets in order to use it later
    with open("listTrained_"+str(time.time()).split('.')[0]+".pkl", 'wb') as f:
        pickle.dump(list(TRAIN_DATA), f)

    # DEBUG purpose
    print("Untreatable "+str(totalUnsablePDF.value)+" over "+str(numberOfPDFfiles.value)+" pdf ("+str(totalUnsablePDF.value/numberOfPDFfiles.value)+")")        


# DEBUG purpose
print("Will train the model over " + str(len(TRAIN_DATA)) + " PDFs")


# By default, en_core_web_md is pre-trained to recognize entities. We will use this one to improve it for our use
nlp = spacy.load("en_core_web_md")

# Get the NER pipeline
ner = nlp.get_pipe("ner")

# Needed if we have added custom label that the model should recognize
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])


# Because en_core_web_md has other capatibilites, we just want to train the NER pipeline
pipe_exceptions = ["ner"]

# Hereafter we will use unaffected_pipes
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]




# TRAINING THE MODEL
# Disable all other pipes (only train NER for now)
with nlp.disable_pipes(*unaffected_pipes):
  
    # DEBUG purpose
    print(nlp.pipe_names)  
    
    # Training for 30 iterations
    for iteration in range(30):

        # Shuufling examples before every iteration
        random.shuffle(TRAIN_DATA)
    
        losses = {}
    
        # Batch up the datasets using spaCy's minibatch
    
        batches = spacy.util.minibatch(TRAIN_DATA, size=spacy.util.compounding(4.0, 32.0, 1.001))
        #batches = spacy.util.minibatch(TRAIN_DATA, size=32)
        for batch in batches:
            for text, annotations in batch:
                
                doc = nlp.make_doc(text)
                try:
                    example = spacy.training.Example.from_dict(doc, annotations)
                except ValueError: # TODO check, a few failed (10)
                    continue
                nlp.update([example], drop=0.5,losses=losses)
                
            # DEBUG purpose
            print("Losses", losses)


# Saving the model
output_dir = Path('ResultV5/') 
nlp.to_disk(output_dir)            