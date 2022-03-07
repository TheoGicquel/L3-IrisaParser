import pdfplumber
import os
import time
from colorama import init, Fore
init() #initialize colorama 
title_debug = False

debug_prefix = Fore.LIGHTBLACK_EX+ "(title)"

import filters
import extract


def parse_dir(directory):
    result = []
    for filename in os.listdir(directory):
        pdf_file_path = os.path.join(directory, filename)
        if(title_debug):print(debug_prefix +Fore.MAGENTA+'[<]INPUT : PARSING "'+pdf_file_path+'"'+ Fore.RESET)

        if os.path.isfile(pdf_file_path):
            with pdfplumber.open(pdf_file_path) as pdf:
                title = parse_title(pdf)
                result.append(title)




def parse_title(pdf:pdfplumber.PDF):
    # get Only 1/3 of pdf's first page
    page = filters.crop_first_page(pdf)
    
    # get text line by line 
    text = page.extract_text(x_tolerance=3, y_tolerance=3)
    # store in list
    lines = text.split('\n')
    
    # remove useless lines and keep only first 5 valid lines
    lines = filters.filter_lines(lines)
    
    # fetch only 5 largest fonts in page
    largest_fonts = extract.get_page_largest_fonts_list(pdf,5)
    
    # only use fonts above threshold
    largest_fonts = filters.filter_fonts(largest_fonts)

    # find in whole page, sequences of text matching largest fonts
    potential_titles = extract.extract_potential_titles(page,largest_fonts)    
    
    # filtering ridiculously long or short files and containing some characters
    potential_titles = filters.filter_potential_titles(potential_titles)
    
    matched = extract.parse_potential_titles(lines,potential_titles)
    
    # filter duplicates
    matched = filters.filter_matches(matched)
    final_title = ''
    ##### FALLBACKS
    errcount = 0
    if(len(matched)>1):
        errcount = errcount +1
        if(title_debug):print(debug_prefix+Fore.BLUE + "[*]WARN : multiple titles ! selecting [0] by default" + Fore.RESET)
        final_title = matched[0]
    
    if(len(matched)==0):
        if(title_debug):print(debug_prefix+Fore.BLUE + "[*]WARN : NO REGULAR TITLE FOUND ! falling back on metadata" + Fore.RESET)
        meta_title = extract.get_title_metadata(pdf)
        if(meta_title is None):
            if(title_debug):print(debug_prefix+Fore.BLUE + "[*]WARN : NO TITLE METADATA FOUND ! falling back on first line..." + Fore.RESET)
            final_title = lines[0]
        else:
            final_title = meta_title

    if(len(matched)==1):
        final_title = matched[0]
    
    if(title_debug):print(debug_prefix+Fore.GREEN + '[>]RESULT : "' + Fore.RESET + final_title + Fore.GREEN + '"\n')
    return final_title
    
if __name__ == '__main__':
    title_debug = True
    time_start = time.time()
    parse_dir('./tests/corpus_large/')
    time_end = time.time()
    if(title_debug):print(debug_prefix+'TIME : '+ Fore.RESET + str(round(time_end-time_start,2)) + 's')