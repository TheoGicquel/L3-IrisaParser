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

def crop_first_page(pdf:pdfplumber.PDF,do_crop=False):
    """Return only first page of pdf"""
    page = pdf.pages[0]
    
    if(do_crop==True):# WARNING : MAY CAUSE BOUNDING BOXES ERROR
        if(title_debug):print(debug_prefix+Fore.BLUE + "[*]WARN : Attemtping to crop page, may cause crash" + Fore.RESET)
        # cropping parameters    
        x0 = 0 # top left corner
        top = 0 # distance from top of page
        x1 = page.width # top right corner
        bottom = float(page.height)/3.0 # distance from bottom of page
        page = page.crop((x0, top, x1, bottom))
    
    return page


def filter_fonts(fonts):
    """Return only fonts above threshold"""
    threshold = 8.0
    res = []
    for font in fonts:
        if(font>threshold):
           res.append(font)
    return res 
    

def filter_potential_titles(titles):
    '''Filter invalid titles (too short,too long)'''
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


def filter_matches(titles):
    test = titles
    res = []
    for i in test:
        i = i.strip() # remove extra spaces at beginning and end
        i = ' '.join(i.split())
        res.append(i) 
    res = list(dict.fromkeys(res))
    return res


def filter_bad_metadata(meta):
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

