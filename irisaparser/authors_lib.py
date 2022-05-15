# -*- coding: utf-8 -*-

import spacy
import re
import pathlib
import pdfplumber
import string
nlp = spacy.load(str(pathlib.Path(__file__).parent.absolute())+'/CustomNER/')
#nlp = spacy.load("en_core_web_md");

def getAffiliations(pdfData,authors,pdfPath):
    pdfData = pdfplumber.open(pdfPath)
    currentPageText2 = pdfData.pages[0].extract_text(x_tolerance=1.8,y_tolerance=2)
    
    affiliations = {}
    
    # Remove unecessary chars in text extracted
    currentPageText2 = re.sub("a´","a",currentPageText2)
    currentPageText2 = re.sub("&\n","and ",currentPageText2)
    currentPageText2 = re.sub("´e","é",currentPageText2)
    currentPageText2 = re.sub("e´","é",currentPageText2)
    currentPageText2 = re.sub("c¸","ç",currentPageText2)
    currentPageText2 = re.sub("ˆı","î",currentPageText2)
    currentPageText2 = re.sub("e`","è",currentPageText2)
    currentPageText2 = re.sub("E´","É",currentPageText2)
    currentPageText2 = re.sub("´","",currentPageText2)

    regexToFindAffiliations = "(?:Univ|LIMSI|CERI|DTIC|Universitat|LIA|Labs|Laboratoire|Ecole|École|Université|University|Département|Department|Institute|DA-IICT|Google|Research|Universidade).*?(?:Canada|Brasil|France|USA|UK|CA|Italy|Aix-Marseille|Mila|India|Austin|Spain|Mexico|Edinburg)"
    indexStartAuthor = -1
    indexEndAuthor = -1
    
    c= currentPageText2.replace("\n"," ")
    c= re.sub(" +"," ",c)
    for auteur in authors[:]:
        indexStartAuthor = currentPageText2.find(auteur)
        indexEndAuthor = indexStartAuthor+len(auteur)
        afterAuthorsStr = currentPageText2[indexEndAuthor:indexEndAuthor+1]
        
        # Method 1
        if afterAuthorsStr not in string.printable:     

            k=re.findall(afterAuthorsStr+" *"+regexToFindAffiliations,c)
            if len(k)!=0: 
                for indexAffiliation in range(len(k)):
                    k[indexAffiliation] = re.sub(afterAuthorsStr+" *","",k[indexAffiliation])
                affiliations[auteur] = k
            authors.remove(auteur)
            continue
       
        # Method 2
        pp = currentPageText2[indexEndAuthor:indexEndAuthor+20]
        v=re.search("[0-9](?:,[0-9])*",pp)
        if v:
            ol = v.group(0).split(",")
            for numberAffi in ol:
                k=re.findall(numberAffi+" *"+regexToFindAffiliations,c)
                if not k:
                    break
                if auteur in affiliations.keys():
                    affiliations[auteur].append(re.sub(numberAffi+" *","",k[0]))
                else:
                    affiliations[auteur] = [re.sub(numberAffi+" *","",k[0])]
            authors.remove(auteur)    
            continue
    
    # Method 3
    k=re.findall(regexToFindAffiliations,c)
    
    if len(k)==1:
        for auteur in authors:
            affiliations[auteur] = [k[0]]
    elif len(k)!=0 and len(k)<=len(authors):
        for affiIndex in range(len(k)):
            affiliations[authors[affiIndex]] = [k[affiIndex]]
    elif len(k)!=0 and len(authors)<len(k):
        for authorIndex in range(len(authors)):
            affiliations[authors[authorIndex]] =[ k[authorIndex]]
    else:
        for auteur in authors:
            affiliations[auteur]=[]
        
                     
    return affiliations







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
    currentPageText = re.sub("e`","è",currentPageText)
    
        
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



def associateMailsWithAuthors(pdfData,auteurs,pageNumber=0):
    
    # Dictionnary that will contain name and list of mails corresponding
    authorsInfos={}

    currentPageText = pdfData.pages[pageNumber].extract_text(x_tolerance=1.8,y_tolerance=2)
    
    # Get all mails
    mailsFound = getMails(currentPageText)
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

    return authorsInfos



def getInformationsAuthors(pdfData,pdfPath):
    
    finalInfos = {}
    
    auteurs = getAuthors(pdfData)
    mails = associateMailsWithAuthors(pdfData,auteurs)
    affiliations = getAffiliations(pdfData,auteurs,pdfPath)
    
    # TODO : do better
    for author,mail in mails.items():
        finalInfos[author] = {"mail":mail}
    for author,affiliation in affiliations.items():
        finalInfos[author]["affiliation"] = affiliation
    
    return finalInfos
