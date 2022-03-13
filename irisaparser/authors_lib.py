import spacy
import re
import pathlib
import pdfplumber
nlp = spacy.load(str(pathlib.Path(__file__).parent.absolute())+'/CustomNER/')

def getMails(text):
    
    # Find all mails within the page
    mailsFound = re.findall(r"[{|(|[[a-zA-Z0-9\.\-+_]+ ?[,;] ?[a-zA-Z0-9\.\-+_]+[}|)|\]]@[a-z0-9\.\-+_]+\.[a-z]+|[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",text)

    # For each mail found with the regex
    for mail in mailsFound:
        
        # Sometimes they are formated like this : {certescertes,ok}@univ-ubs.fr | so there are multiple mails
        if "," in mail or ";" in mail:
            
            # Example : modifiedMail = [ "{certescertes,ok}" , "univ-ubs.fr" ]
            modifiedMail = mail.replace(" ","").split("@")
            
            
            # For each mail separated by "," or ";"
            for newMail in re.split(r';|,', modifiedMail[0][1:-1]):
                # Add it to the new list of mail
                mailsFound.append(newMail + "@" + modifiedMail[-1])
                
            # Remove the long mail from the list founded by the regex
            mailsFound.remove(mail)
            
    return mailsFound

def getAuthors(pdfData,pageNumber=0):
    
    #pdfData = pdfplumber.open(pdfFilePathTitle)
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
            #print("ERR : ",pdfFilePathTitle)
            return []
        except ValueError:
            #print("ERR : ",pdfFilePathTitle)
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
        return getAuthors(pdfData,1) # Recursive call

    return namesFound


def getAuthorsInfos(pdfFileName,pageNumber=0):
    
    # Dictionnary that will contain name and list of mails corresponding
    authorsInfos={}
    
    pdfData = pdfplumber.open(pdfFileName)
    currentPageText = pdfData.pages[pageNumber].extract_text(x_tolerance=1.8,y_tolerance=2)
    
    # Get all mails
    mailsFound = getMails(currentPageText)
    
    # Get all authors
    auteurs = getAuthors(pdfData)
    
    nothingFound = True
    for auteur in auteurs:
        authorsInfos[auteur]=["",]
        for partsInName in re.split(r'[ -_]',auteur):
            for mail in mailsFound:
                if len(partsInName)>=3 and mail.lower().find(partsInName.lower()) != -1:
                    nothingFound = False
                    if authorsInfos.get(auteur)[0]!="":
                        authorsInfos[auteur].append(mail)
                    else:
                        authorsInfos[auteur]=[mail,]
                    mailsFound.remove(mail)

    if pageNumber==0 and nothingFound:
        return getAuthorsInfos(pdfFileName,1)
    elif pageNumber==1 and nothingFound:
        return getAuthorsInfos(pdfFileName,len(pdfData.pages)-1)
    return authorsInfos


# Example of use
if __name__ == "__main__":
    print(getAuthorsInfos("339946AC27C12253960F8BF99F2C033EC01CB585/jne11_4_046009.pdf"))
    """
    import glob
    allFiles = glob.glob("**/*.pdf")
    for pdfFileName in allFiles:
        print("[+] ",pdfFileName)
        print(getAuthorsInfos(pdfFileName))
        print()
    """
