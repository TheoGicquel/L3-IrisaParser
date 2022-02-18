from argparse import ArgumentError
import logging

from time import time

import pdfplumber
import os
import colorama
from colorama import init,Fore,Back,Style
import time

init() #initialize colorama 
import logging

log = logging.getLogger(__name__)


#################### INPUT / COMMON ####################
'''
Used to fetch files from filesystem and perform parsing
for each file in specified directory
'''

def parseDir(directory):
    result = []
    for filename in os.listdir(directory):
        pdf_file_path = os.path.join(directory, filename)
        print(Fore.MAGENTA + '[<]INPUT : PARSING "'+pdf_file_path+'"' + Fore.RESET)

        if os.path.isfile(pdf_file_path):
            with pdfplumber.open(pdf_file_path) as pdf:
                title = parseTitle(pdf)
                result.append(title)

#################### FILTERS / CROP ####################

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
        # cropping parameters    
        x0 = 0 # top left corner
        top = 0 # distance from top of page
        x1 = page.width # top right corner
        bottom = float(page.height)/3.0 # distance from bottom of page
        page = page.crop((x0, top, x1, bottom))
    
    return page


def filterFonts(fonts):
    """Return only fonts above threshold"""
    threshold = 8.0
    res = []
    for font in fonts:
        if(font>threshold):
           res.append(font)
    return res 
    

def filter_potential_titles(titles):
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
    log.debug("filtered matches :" + str(res))
    return res


def filter_matches(titles):
    res = titles
    for i in res:
        i = i.strip()
        i = ''.join(i.split())
    res = list(dict.fromkeys(res))
    return res

#################### PARSING ####################

def get_sentences(pdf: pdfplumber.PDF,max_sentences,font_list):
    """ return array with x largest sentences in pdf file """
    res = []
    page = pdf.pages[0]

    num_sentences = len(font_list)
    i = 0
    potent_title = ''
    while i < num_sentences:
        for char in page.chars:
            if(char.get('size') == font_list[i]):
                potent_title += char.get('text')
        res.append(potent_title)
        potent_title=''
        i = i + 1

    return res  

def getPageLargestFontsList(page,fontAmount):
    """ Return array with x largest lines in page """
    res = {}
    font_list_uniq = []
    current_font=0.0
    page_fonts = []
    # find every fonts in page
    for char in page.chars:
        scan = round(char.get('size'),4)
        # only add to list fonts that are different 
        if scan not in page_fonts:
            page_fonts.append(scan)
    
    # sort fonts from largest to smallest
    page_fonts.sort(reverse=True)
    page_fonts = page_fonts[:fontAmount-1]
    
    return page_fonts


def extract_potential_titles(page,largestFonts):
    sentences = []
    for font in largestFonts:
        scan = ''
        for char in page.chars:
            if(round(char.get('size'),4) == font):
                scan = scan + char.get('text')
        sentences.append(scan)
    return sentences


def parse_potential_titles(lines,potential_titles):
    res = []
    for pot_title in potential_titles:
        prev = ''
        for line in lines:
            raw_title = pot_title.replace(" ", "")
            raw_line = line.replace(" ", "")

                        
            #print(Fore.BLUE + 'raw : "' + Fore.RESET + raw_title + Fore.BLUE + '"\n' + Fore.RESET, end=' ')
            #print(Fore.CYAN + 'line : "' + Fore.RESET + raw_line + Fore.CYAN + '"\n' + Fore.RESET)
            if(raw_line==raw_title):
                res.append(line)
            # try with previous iteration
            prev_raw = prev.replace(" ", "")
            concat_prev = prev_raw + raw_line
            if(concat_prev == raw_title):
                res.append((prev + " " + line))
            prev=line
                
    return res

def get_title_metadata(pdf:pdfplumber.PDF):
    meta_title=pdf.metadata.get('Title')
    if(meta_title is None or (len(meta_title.strip())==0)):
        print(Fore.RED + "[*]ERROR : NO VALID METADATA FOUND" + Fore.RESET)
        return None
    else:
        return meta_title
    
def parseTitle(pdf:pdfplumber.PDF):
    # get Only 1/3 of pdf's first page
    page = crop_first_page(pdf)
    
    # get text line by line 
    text = page.extract_text()
    # store in list
    lines = text.split('\n')
    
    # remove useless lines and keep only first 5 valid lines
    lines = filter_lines(lines)
    
    # fetch only 5 largest fonts in page
    largestFonts = getPageLargestFontsList(pdf,5)
    
    # only use fonts above threshold
    largestFonts = filterFonts(largestFonts)

    # find in whole page, sequences of text matching largest fonts
    potential_titles = extract_potential_titles(page,largestFonts)    
    
    # filtering ridiculously long or short files and containing some characters
    potential_titles = filter_potential_titles(potential_titles)
    
    matched = parse_potential_titles(lines,potential_titles)
    
    # filter duplicates
    matched = filter_matches(matched)
    final_title = ''
    errcount = 0
    if(len(matched)>1):
        errcount = errcount +1
        print(Fore.BLUE + "[*]WARN : multiple titles ! selecting [0] by default" + Fore.RESET)
        final_title = matched[0]
    
    if(len(matched)==0):
        print(Fore.BLUE + "[*]WARN : NO REGULAR TITLE FOUND ! falling back on metadata" + Fore.RESET)
        meta_title = get_title_metadata(pdf)
        if(meta_title is None):
            print(Fore.BLUE + "[*]WARN : NO TITLE METADATA FOUND ! falling back on first line..." + Fore.RESET)
            final_title = lines[0]

    if(len(matched)==1):
        final_title = matched[0]
    
    print(Fore.GREEN + '[>]RESULT : "' + Fore.RESET + final_title + Fore.GREEN + '"\n')
    return final_title
    
    




if __name__ == '__main__':
    time_start = time.time()
    parseDir('./tests/corpus/')
    time_end = time.time()
    print('TIME : ' + str(round(time_end-time_start,2)) + 's')