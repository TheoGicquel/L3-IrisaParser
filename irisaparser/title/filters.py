import pdfplumber
title_debug = False
from colorama import init,Fore
debug_prefix = Fore.LIGHTBLACK_EX+ "(title)"


def filter_lines(line_list):
    res=[]
    for line in line_list:
        valid = True
        # catching incorrect lines
        if(len(line)<2):
            valid = False
                
        # final check
        if(valid == True):
            res.append(line)
    # return only first 5 valid lines
    return res[:5]


def filter_fonts(fonts):
    """Return only fonts above threshold"""
    threshold = 8.0
    res = []
    for font in fonts:
        if(font>threshold):
           res.append(font)
    return res 
    

def filter_potential_titles(titles):
    """Filter invalid titles (too short,too long)"""
    res = []
    
    for title in titles:
        valid = True
        char_only = str(title).strip()
        lenght = len(char_only)
        
        if(lenght<2 or lenght>80):
            valid = False
            
        # catch wrong titles
        if(valid==True):
            res.append(title)
    return res


def filter_duplicates(titles):
    test = titles
    res = []
    for i in test:
        i = i.strip() # remove extra spaces at beginning and end
        i = ' '.join(i.split())
        res.append(i) 
    res = list(dict.fromkeys(res))
    return res


def filter_bad_metadata(meta):
    #!TODO REFACTOR INTO extract.title()
    if(meta==None):
        return None
    if(len(meta.strip())<5):
        return None
    if("/" in meta):
        return None
    if('\\' in meta):
        return None
    if("(" in meta):
        return None
    if(")" in meta):
        return None
    return meta

