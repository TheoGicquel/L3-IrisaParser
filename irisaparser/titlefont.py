from argparse import ArgumentError
import logging
import pdfplumber
import json
import os
import colorama
from colorama import init,Fore,Back,Style
init() #initialize colorama 

###############################################################################
def extract(input_path):
    """
    Attempt to extract title from pdf file using pdfplumber and various methods
    """
    with pdfplumber.open(input_path) as pdf:
        print('[*] "' + input_path + '"')
        title = get_title_from_font(pdf)
    return title

###############################################################################

def get_title_from_font(pdf: pdfplumber.PDF,max_pages=1,max_fonts=3):
    if((max_pages > len(pdf.pages))):
        raise ArgumentError('Page amount larger than pdf page count')
    if(max_pages < 1 ):
        raise ArgumentError('must be at least 1 page')
    if(max_fonts < 1):
        raise ArgumentError('must be at least 1 font')
    
    get_largest_font_sizes_dict(pdf,max_pages=max_pages,max_fonts=max_fonts)




def get_largest_font_pages(pdf: pdfplumber.PDF,max_pages):
    """ return largest font in x first pages of pdf file"""
    res = 0;
    for page in pdf.pages[:max_pages]:
        for char in page.chars:
            curchar_size = char.get('size')
            if(curchar_size > res):
                res = curchar_size
    return res




def get_largest_lines(pdf: pdfplumber.PDF,max_fonts,max_pages,largest_font):
    """ Return array with x largest lines in pdf file """
    res = {}
    print('\t[get_largest_lines]')
    for page in pdf.pages[:max_pages]:
        print( '\t\t' + '"' + Fore.GREEN  ,end='')
        for char in page.chars:
            if(char.get('size')==largest_font):
                print('' + char.get('text'),end='')
            
    print(Fore.RESET+ '"')
    return res





def get_largest_font_sizes_dict(pdf: pdfplumber.PDF,max_fonts,max_pages):
    """ Fetch largest font in first 'max_pages' pages of pdf file """
    res = {}
    largest = get_largest_font_pages(pdf=pdf,max_pages=max_pages)
    print('\tlargest font in pg[' + '1-' + str(max_pages) + '] :'  + str(round(largest,2)) + 'pt')
    res = get_largest_lines(pdf=pdf,max_fonts=max_fonts,max_pages=max_pages,largest_font=largest)
    
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
    debug('./tests/corpus/')
