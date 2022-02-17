from argparse import ArgumentError
import logging
from operator import truediv
from time import time
from traceback import print_tb
import pdfplumber
import json
import os
import colorama
from colorama import init,Fore,Back,Style
import time
init() #initialize colorama 

###############################################################################
def extract(input_path):
    """
    Attempt to extract title from pdf file using pdfplumber and various methods
    """
    with pdfplumber.open(input_path) as pdf:
        print('\n\n[*] "' + input_path + '"')
        titles = get_title_from_font(pdf)
        accurate = []
        for title in titles:
            if(len(title)<90 and len(title)>20):
                print(Fore.BLUE + 'Potential title found : ' + Fore.RESET + '"' + title + '"' + '(' + str(len(title)) + ')')
                accurate.append(title)
        text = pdf.pages[0].extract_text()

        lines = text.split('\n')
        lines = filter_lines(lines)
        #print(Fore.BLUE + 'Extracted text : ' + Fore.RESET + '"' + lines[0] + '"' + '(' + str(len(text)) + ')')
        title = line_potential_line_matcher(lines,accurate)
    return title

###############################################################################

def filter_lines(lines):
    line_list = lines[0:10]
    res = []

    for line in line_list:
        if(len(line)<80):
            res.append(line)
    return res
    
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
    print(res)

def get_title_from_font(pdf: pdfplumber.PDF,max_pages=1,max_fonts=3):
    if((max_pages > len(pdf.pages))):
        raise ArgumentError('Page amount larger than pdf page count')
    if(max_pages < 1 ):
        raise ArgumentError('must be at least 1 page')
    if(max_fonts < 1):
        raise ArgumentError('must be at least 1 font')
    
    res = get_largest_font_sizes_dict(pdf,max_pages=max_pages,max_fonts=max_fonts)

    return res


def get_largest_font_pages(pdf: pdfplumber.PDF,max_pages):
    """ return largest font in x first pages of pdf file"""
    res = 0;
    for page in pdf.pages[:max_pages]:
        for char in page.chars:
            curchar_size = char.get('size')
            if(curchar_size > res):
                res = curchar_size
    return res




def get_largest_font_list(pdf: pdfplumber.PDF,max_fonts,max_pages,largest_font):
    """ Return array with x largest lines in pdf file """
    res = {}
    font_list_uniq = []
    current_font =0
    for page in pdf.pages[:max_pages]:
        #print( '\t\t' + '"' + Fore.GREEN  ,end='')
        for char in page.chars:
            if(char.get('size')!=current_font):
                current_font = char.get('size')
                font_list_uniq.append(char.get('size'))
    
    font_list_uniq.sort(reverse=True)
    font_list_uniq = remove_duplicate_entries(font_list_uniq)                        
    font_list_uniq = font_list_uniq[:max_fonts]
    
    return font_list_uniq



def remove_duplicate_entries(font_list):
    res = font_list
    res = list(dict.fromkeys(res))
    return res

def get_largest_font_sizes_dict(pdf: pdfplumber.PDF,max_fonts,max_pages):
    """ Fetch largest fonts in first 'max_pages' pages of pdf file """
    largest_font = get_largest_font_pages(pdf=pdf,max_pages=max_pages)
    #print('\tlargest font in pg[' + '1-' + str(max_pages) + '] :'  + str(round(largest,2)) + 'pt')
    largest_fonts = get_largest_font_list(pdf=pdf,max_fonts=max_fonts,max_pages=max_pages,largest_font=largest_font)
    sentences = get_sentences(pdf=pdf,max_sentences=max_fonts,font_list=largest_fonts)
    
    return sentences
    
def crop_first_page(page):
    


def get_sentences(pdf: pdfplumber.PDF,max_sentences,font_list):
    """ return array with x largest sentences in pdf file """
    res = []
    page = pdf.pages[0]
    #(x0, top, x1, bottom)
    x0 = 0
    top = 0
    x1 = page.width
    bottom = float(page.height)/3
    top_page = page.crop((x0, top, x1, bottom))
    #im = top_page.to_image(resolution=150)
    #im.save("bottom.png", format="PNG")
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




###############################################################################

# UNUSED
def get_largest_font_sizes_dict_old(pdf: pdfplumber.PDF):
    largest_sentences = []
    current_font_size = 0.0
    matches = 0
    sentence = ''
    largest_fonts = []
    max_sentences = 3
    while matches < max_sentences:
        for page in pdf.pages[0:1]:
            for obj in page.chars[0:300]:
                sentence += obj.get('text')
                if(obj.get('size')) != current_font_size:
                    matches = matches + 1
                    largest_sentences.append(sentence)
                    largest_fonts.append(obj.get('size'))
                    sentence = ''
                    current_font_size = obj.get('size')
                    #print('['+ Fore.YELLOW + str(round(current_font_size,2)) + 'pt' + Fore.RESET + ']')
    
    for sentence in largest_sentences:
        print('Found large text : "' + Fore.BLUE + sentence + Fore.RESET + '"')
    for font in largest_fonts:
        print('Found large font : ' + Fore.YELLOW + str(round(font,2)) + Fore.RESET + 'pt')
 

 
###############################################################################
    
def debug(directory):
    """ Attempt title extraction of titles of all pdf files in specified directory

    Args:
        directory (string): path to directory containing pdf files
    """
    meta_missing = 0 # count of files without metadata
    count = 0 # count of pdf files processed
    meta_no_match = 0 # amount of titles not matching with metadata
    lenght = 50 # max lenght of title to display
    tab = '\t' # tab for formatting
    disp_meta = True
    disp_line = True
    print('')
    print("[RUNNING irisaparser.title.debug()]")
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            count = count + 1
            title = extract(f)
    '''
            print('['+ str(count) + ']',end=tab)
            #print(Fore.CYAN + 'font : ' + title[0:lenght] + '..' + Fore.RESET)


    print("== summary == ")
    print("total pdf files \t\t: " + Fore.YELLOW + str(count) + Fore.RESET)
    print("w/o title metadata \t\t: " + Fore.RED + str(meta_missing) + Fore.RESET + "/" + str(count) + " (" + str(round(meta_missing/count*100,1)) + "%)")
    print("w/o title as first line \t: " + Fore.RED +  str(meta_no_match) + Fore.RESET + "/" + str(count) + " (" + str(round(meta_no_match/count*100,1)) + "%)")
    print("== end summary == ")
    print("")
    '''




if __name__ == '__main__':
    time_start = time.time()
    debug('./tests/single/')
    time_end = time.time()
    print('TIME : ' + str(round(time_end-time_start,2)) + 's')