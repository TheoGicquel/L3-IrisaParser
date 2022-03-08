import pdfplumber
from colorama import init,Fore
debug_prefix = Fore.LIGHTBLACK_EX+ "(title)"
title_debug = False
import filters

def largest_titles(pdf: pdfplumber.PDF,max_sentences,font_list):
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




def largest_fonts(page,font_amount):
    """ Return array with x largest fonts in page """

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


def largest_titles(page,largest_fonts):
    sentences = []
    for font in largest_fonts:
        scan = ''
        for char in page.chars:
            if(round(char.get('size'),4) == font):
                scan = scan + char.get('text')
        sentences.append(scan)
    return sentences


def parse_potential_titles(lines_input,potential_titles):
    #!TODO CLEANUP / COMMENT
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



def title_metadata(pdf:pdfplumber.PDF):
    """"""
    #!TODO INCLUDE FILTERS DIRECTLY INTO FUNCTION
    meta_title=pdf.metadata.get('Title')
    meta_title=meta_title.strip()
    if(len(meta_title)<5):
        return None

    invalid_chars=['/','\\','(',')',]
    
    for c in meta_title:
        if c in invalid_chars:
            return None


    if(meta_title is None):
        if(title_debug):print(debug_prefix+Fore.RED + "[*]ERROR : NO VALID METADATA FOUND" + Fore.RESET)
        return None
    
    return meta_title
    
