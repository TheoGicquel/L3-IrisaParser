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
                title = parse_title(pdf)
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
    log.debug("filtered matches :" + str(res))
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

def get_page_largest_fonts_list(page,font_amount):
    """ Return array with x largest lines in page """

    page_fonts = []
    # find every fonts in page
    for char in page.chars:
        scan = round(char.get('size'),4)
        # only add to list fonts that are different 
        if scan not in page_fonts:
            page_fonts.append(scan)
    
    # sort fonts from largest to smallest
    page_fonts.sort(reverse=True)
    page_fonts = page_fonts[:font_amount-1]
    
    return page_fonts


def extract_potential_titles(page,largest_fonts):
    sentences = []
    for font in largest_fonts:
        scan = ''
        for char in page.chars:
            if(round(char.get('size'),4) == font):
                scan = scan + char.get('text')
        sentences.append(scan)
    return sentences


def parse_potential_titles(lines_input,potential_titles):
    lines = lines_input
    res = []
    for pot_title in potential_titles:
        prev = ''
        for line in lines:
            raw_title = pot_title.replace(" ", "")
            raw_line = line.replace(" ", "")

            if(raw_line==raw_title):
                res.append(line)
            # try with previous iteration
            prev_raw = prev.replace(" ", "")
            concat_prev = prev_raw + raw_line
            if(concat_prev == raw_title):
                res.append((prev + " " + line))
            prev=line
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



def get_title_metadata(pdf:pdfplumber.PDF):
    meta_title=pdf.metadata.get('Title')
    meta_title=filter_bad_metadata(meta_title)
    if(meta_title is None):
        print(Fore.RED + "[*]ERROR : NO VALID METADATA FOUND" + Fore.RESET)
        return None
    
    return meta_title
    
def parse_title(pdf:pdfplumber.PDF):
    # get Only 1/3 of pdf's first page
    page = crop_first_page(pdf)
    
    # get text line by line 
    text = page.extract_text(x_tolerance=3, y_tolerance=3)
    # store in list
    lines = text.split('\n')
    
    # remove useless lines and keep only first 5 valid lines
    lines = filter_lines(lines)
    
    # fetch only 5 largest fonts in page
    largest_fonts = get_page_largest_fonts_list(pdf,5)
    
    # only use fonts above threshold
    largest_fonts = filterFonts(largest_fonts)

    # find in whole page, sequences of text matching largest fonts
    potential_titles = extract_potential_titles(page,largest_fonts)    
    
    # filtering ridiculously long or short files and containing some characters
    potential_titles = filter_potential_titles(potential_titles)
    
    matched = parse_potential_titles(lines,potential_titles)
    
    # filter duplicates
    matched = filter_matches(matched)
    final_title = ''
    ##### FALLBACKS
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
        else:
            final_title = meta_title

    if(len(matched)==1):
        final_title = matched[0]
    
    print(Fore.GREEN + '[>]RESULT : "' + Fore.RESET + final_title + Fore.GREEN + '"\n')
    return final_title
    
    




if __name__ == '__main__':
    time_start = time.time()
    parseDir('./tests/corpus/')
    time_end = time.time()
    print('TIME : ' + str(round(time_end-time_start,2)) + 's')