import pdfplumber
import spacy
import re
from pathlib import Path

nlp = spacy.load(Path('CustomNER/'))


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
            namesFound.append(ent.text.strip())
    
    # In some PDF, the first page is a cover page so we have to check the next page
    if not namesFound and pageNumber==0:
        return getAuthors(pdfFilePathTitle,1) # Recursive call

    return namesFound

# Example of use
if __name__ == "__main__":
    print(getAuthors("Das_Martins.pdf"))
