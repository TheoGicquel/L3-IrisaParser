# -*- coding: utf-8 -*-

import spacy
import re
import pathlib
import pdfplumber
import string
import unicodedata

nlp = spacy.load(str(pathlib.Path(__file__).parent.absolute())+'/CustomNER/')

def getAffiliations(pdfData,authors,pdfPath,pageNumber=0):
    
    pdfData = pdfplumber.open(pdfPath)
    currentPageText = pdfData.pages[pageNumber].extract_text(x_tolerance=1.8,y_tolerance=2)
    
    affiliations = {}
    
    # Remove unecessary chars in text extracted
    currentPageText = re.sub("a´","a",currentPageText)
    currentPageText = re.sub("&\n","and ",currentPageText)
    currentPageText = re.sub("´e","é",currentPageText)
    currentPageText = re.sub("e´","é",currentPageText)
    currentPageText = re.sub("c¸","ç",currentPageText)
    currentPageText = re.sub("ˆı","î",currentPageText)
    currentPageText = re.sub("e`","è",currentPageText)
    currentPageText = re.sub("E´","É",currentPageText)
    currentPageText = re.sub("´","",currentPageText)
    currentPageText = re.sub("ﬁ","fi",currentPageText)

    regexToFindAffiliations = "(?:Univ|LIMSI|CERI|DTIC|Universidade|Universitat|LIA|INRIA|LIRMM|Labs|Laboratoire|Ecole|École|Université|University|Département|Department|Institute|DA-IICT|Google|Research|Universidade).*?(?:Canada|Brasil|France|USA|UK|CA|Italy|Aix-Marseille|Mila|India|Austin|Spain|Mexico|Edinburgh)"
    indexStartAuthor = -1
    indexEndAuthor = -1
    
    c = currentPageText.replace("\n"," ")
    c = re.sub(" +"," ",c)
    
    for auteur in authors[:]:
        indexStartAuthor = currentPageText.find(auteur)
        indexEndAuthor = indexStartAuthor+len(auteur)
        afterAuthorsStr = currentPageText[indexEndAuthor:indexEndAuthor+1]
        
        # Method 1
        if afterAuthorsStr not in string.printable: # If the chars following is not in ACSII range (often to index a specific affiliation that will begin with the same non ASCII char)

            affiliationsFind=re.findall(afterAuthorsStr+" *"+regexToFindAffiliations,c)
            if len(affiliationsFind)!=0: 
                for indexAffiliation in range(len(affiliationsFind)):
                    affiliationsFind[indexAffiliation] = re.sub(afterAuthorsStr+" *","",affiliationsFind[indexAffiliation])
                affiliations[auteur] = affiliationsFind
            authors.remove(auteur)
            continue
       
        # Method 2
        strFollowingAuthor = currentPageText[indexEndAuthor:indexEndAuthor+20] # Some times numbers are following the author in order to  index a specific affiliation that will begin with the same number
        affiliationsFounded=re.search("[0-9](?:,[0-9])*",strFollowingAuthor)
        if affiliationsFounded:
            listOfNumbers = affiliationsFounded.group(0).split(",") # Sometimes multiple affiliations : 1,2,3,*
            for numberAffi in listOfNumbers:
                affiliationsFind =re.findall(numberAffi+" *"+regexToFindAffiliations,c)
                if not affiliationsFind:
                    break
                if auteur in affiliations.keys():
                    affiliations[auteur].append(re.sub(numberAffi+" *","",affiliationsFind[0]))
                else:
                    affiliations[auteur] = [re.sub(numberAffi+" *","",affiliationsFind[0])]
            authors.remove(auteur)    
            continue
    
    # Method 3
    affiFounds=re.findall(regexToFindAffiliations,c)
    
    if len(affiFounds)==1:
        for auteur in authors:
            affiliations[auteur] = [affiFounds[0]]
    elif len(affiFounds)!=0 and len(affiFounds)<=len(authors):
        for affiIndex in range(len(affiFounds)):
            affiliations[authors[affiIndex]] = [affiFounds[affiIndex]]
    elif len(affiFounds)!=0 and len(authors)<len(affiFounds):
        for authorIndex in range(len(authors)):
            affiliations[authors[authorIndex]] =[ affiFounds[authorIndex]]
    else:
        for auteur in authors:
            affiliations[auteur]=[""]
        
                     
    return affiliations

def getMails(pdfData,pageNumber):
    
    text = pdfData.pages[pageNumber].extract_text(x_tolerance=1.8,y_tolerance=2)
    text = text.replace("-\n","")
    # Find all mails within the page
    mailsFound = re.findall(r"[{|(|\[]?(?:[a-zA-Z0-9\.\-+_]+ *[,;] *[a-zA-Z0-9\.\-+_]+)+[\]|)|}]?@[a-zA-Z0-9\.\-+_]+\.[a-zA-Z]+|[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",text)
    # For each mail found with the regex
    for mail in mailsFound:
        
        # Sometimes they are formated like this : {certescertes,ok}@univ-ubs.fr | so there are multiple mails
        if "," in mail or ";" in mail:
            
            # Example : modifiedMail = [ "{certescertes,ok}" , "univ-ubs.fr" ]
            modifiedMail = mail.replace(" ","").split("@")
            
            # Remove extra chars
            modifiedMail[0] = re.sub(r'^[{|(|\[]|[}|)|\]]$',"", modifiedMail[0] )
            
            # For each mail separated by "," or ";"
            for newMail in re.split(r';|,', modifiedMail[0]):
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
    currentPageText = re.sub("e`","è",currentPageText)
    currentPageText = re.sub("ﬁ","fi",currentPageText)
    
    
        
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
    return (namesFound,pageNumber)

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def associateMailsWithAuthors(pdfData,auteurs,pdfPath,pageNumber=0):
    
    # Dictionnary that will contain name and list of mails corresponding
    authorsInfos={}
    pdfData = pdfplumber.open(pdfPath)
    
    # Get all mails
    mailsFound = getMails(pdfData,pageNumber)
    for auteur in auteurs:
        auteurNorm = strip_accents(auteur)
        nothingFound = True
        authorsInfos[auteur]=["",]
        for partsInName in re.split(r' |-|_',auteurNorm):
            for mail in mailsFound:
                if len(partsInName)>=2 and (mail.lower().find(partsInName.lower()) != -1 ):
                    nothingFound = False
                    authorsInfos[auteur]=[mail,]
                    mailsFound.remove(mail)
                    break
            if not nothingFound:
                break
            
    return authorsInfos

def getInformationsAuthors(pdfData,pdfPath):
    
    finalInfos = {}
    
    auteurs , pageWhereAuthorsGetted = getAuthors(pdfData)
    mails = associateMailsWithAuthors(pdfData,auteurs,pdfPath,pageWhereAuthorsGetted)
    affiliations = getAffiliations(pdfData,auteurs,pdfPath,pageWhereAuthorsGetted)
    
    # TODO : do better
    for author,mail in mails.items():
        finalInfos[author] = {"mail":mail}
    for author,affiliation in affiliations.items():
        finalInfos[author]["affiliation"] = affiliation
    
    return finalInfos
