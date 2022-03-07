import pdfplumber
import os
import time
from colorama import init, Fore
init() #initialize colorama 
title_debug = False

debug_prefix = Fore.LIGHTBLACK_EX+ "(title)"

import filters
import extract

def parse_title(pdf:pdfplumber.PDF):
    # get Only 1/3 of pdf's first page
    page = pdf.pages[0]
    
    # get text line by line 
    text = page.extract_text(x_tolerance=3, y_tolerance=3)
    # store in list
    lines = text.split('\n')
    
    # remove useless lines and keep only first 5 valid lines
    lines = filters.filter_lines(lines)
    
    # fetch only 5 largest fonts in page
    largest_fonts = extract.largest_fonts(pdf,5)
    
    # only use fonts above threshold
    largest_fonts = filters.filter_fonts(largest_fonts)

    # find in whole page, sequences of text matching largest fonts
    potential_titles = extract.largest_titles(page,largest_fonts)    
    
    # filtering ridiculously long or short files and containing some characters
    potential_titles = filters.filter_potential_titles(potential_titles)
    
    matched = extract.parse_potential_titles(lines,potential_titles)
    
    # filter duplicates
    matched = filters.filter_duplicates(matched)
    final_title = ''
    ##### FALLBACKS
    errcount = 0
    if(len(matched)>1): # more than one title found -> keep largest one
        errcount = errcount +1
        if(title_debug):print(debug_prefix+Fore.BLUE + "[*]WARN : multiple titles ! selecting [0] by default" + Fore.RESET)
        final_title = matched[0]

    if(len(matched)==1):
        final_title = matched[0]
    
    if(len(matched)==0): # title not found -> consult metadata -> if not accurate, first line is used
        if(title_debug):print(debug_prefix+Fore.BLUE + "[*]WARN : NO REGULAR TITLE FOUND ! falling back on metadata" + Fore.RESET)
        meta_title = extract.title_metadata(pdf)
        if(meta_title is None):
            if(title_debug):print(debug_prefix+Fore.BLUE + "[*]WARN : NO TITLE METADATA FOUND ! falling back on first line..." + Fore.RESET)
            final_title = lines[0]
        else:
            final_title = meta_title
    
    if(title_debug):print(debug_prefix+Fore.GREEN + '[>]RESULT : "' + Fore.RESET + final_title + Fore.GREEN + '"\n')
    
    return final_title
