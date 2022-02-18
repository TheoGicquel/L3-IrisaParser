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
import logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
log.info('imported title final')


#################### INPUT / COMMON ####################
'''
Used to fetch files from filesystem and perform parsing
for each file in specified directory
'''

def parseDir(directory):
    for filename in os.listdir(directory):
        pdf_file_path = os.path.join(directory, filename)
        log.info('now parsing ' + pdf_file_path)
        if os.path.isfile(pdf_file_path):
            with pdfplumber.open(pdf_file_path) as pdf:
                title = parseTitle(pdf)

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
    return res

#################### PARSING ####################

    
def line_potential_line_matcher(lines,potential_title):
    sentence = ''
    res = []
    for p_title in potential_title:
        for line in lines:
            scan = line.strip()
            if(p_title.find(scan)):
                sentence = sentence + line + ' '
        res.append(sentence)
        sentence = ''
    print(Fore.CYAN + 'matches : ' + Fore.RESET,end='')
    print(res)




def get_sentences(pdf: pdfplumber.PDF,max_sentences,font_list):
    """ return array with x largest sentences in pdf file """
    res = []
    page = pdf.pages[0]

    num_sentences = len(font_list)
    i = 0
    potent_title = ''
    while i < num_sentences:
        for char in page.chars:
            #print('i:' + str(i) + ' char: ' + char.get('text'))         
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

    # find in whole page, sequences containing largest fonts
    potential_titles = extract_potential_titles(page,largestFonts)    
    
    potential_titles = filter_potential_titles(potential_titles)
    print(potential_titles)
    final_title=''
    return final_title
    
    




if __name__ == '__main__':
    time_start = time.time()
    parseDir('./tests/corpus/')
    time_end = time.time()
    print('TIME : ' + str(round(time_end-time_start,2)) + 's')