from turtle import title
from black import out
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
        meta_title = extract_from_metadata(pdf)
        first_line = extract_first_line(pdf)
        font_size = extract_from_font_size(pdf)
    return meta_title,first_line,font_size

###############################################################################
def extract_from_metadata(plumbed: pdfplumber.PDF):
    """Returns 'Title' attribute from pdf metadata"""
    output_upper = plumbed.metadata.get('Title')
    output_lower = plumbed.metadata.get('title')
    if(output_upper is not None):
        return output_upper
    if(output_lower is not None):
        return output_lower
    if(output_lower == None and output_lower == None):
        return 'NULL'
        
        
###############################################################################

def extract_first_line(plumbed: pdfplumber.PDF):
    """ Fetch first line of pdf file using builtin pdfplumber extract_text() method"""
    title_page_chars = plumbed.pages[0] # only first page used
    filtered = title_page_chars.extract_text(x_tolerance=3, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
    return(filtered.split('\n')[0])

###############################################################################
def extract_from_font_size(pdf: pdfplumber.PDF):
    """ 
    Extract title by finding the largest font size in first page 
    
    """
    precision = 1
    output = ''
    largest_font = get_largest_font_size(pdf)
    title_page = pdf.pages[0]
    title_page_chars = pdf.pages[0].chars
    
    for i in title_page_chars:
        if (i['size'] - largest_font < precision) and (i['size'] - largest_font > -precision):
            output += str(i['text'])

    return output


def get_largest_font_size(plumbed: pdfplumber.PDF):
    title_page_chars = plumbed.pages[0].chars # only first page used
    largest_font = 0.0
    for i in title_page_chars:
        if(i['size'] > largest_font):
            largest_font = i['size']
    return largest_font    
###############################################################################
    
def debug(directory):
    """ Attempt title extraction of titles of all pdf files in specified directory

    Args:
        directory (string): path to directory containing pdf files
    """
    meta_missing = 0 # count of files without metadata
    count = 0 # count of pdf files processed
    meta_no_match = 0 # amount of titles not matching with metadata
    lenght = 25 # max lenght of title to display
    tab = '\t' # tab for formatting
    print('')
    print("[RUNNING irisaparser.title.debug()]")
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            count = count + 1
            title_meta,title_line,title_font_extracted = extract(f)
            
            print('['+ str(count) + ']',end=tab)
            
            # metadata
            if(title_meta == 'NULL' or title_meta==''):
                print(Fore.RED + 'meta : N/A' + Fore.RESET,end=tab)
                meta_missing = meta_missing + 1
            else:
                print(Fore.GREEN + 'meta : ' + title_meta[0:lenght] + '..' + Fore.RESET,end=tab)
            
            # first line
            if(title_line == 'NULL' or title_line==''):
                print(Fore.RED + 'line : N/A' + Fore.RESET,end=tab)
            else:
                print(Fore.MAGENTA + 'line : ' + title_line[0:lenght] + '..' + Fore.RESET,end=tab)
            # first line matching meta
            if(title_line!=title_meta):
                meta_no_match = meta_no_match + 1
            
            # font size
            print(Fore.CYAN + 'font : ' + title_font_extracted[0:lenght] + '..' + Fore.RESET)
            


    print("== summary == ")
    print("total pdf files \t\t: " + Fore.YELLOW + str(count) + Fore.RESET)
    print("w/o title metadata \t\t: " + Fore.RED + str(meta_missing) + Fore.RESET + "/" + str(count))
    print("w/o matching metadata & title \t: " + Fore.RED +  str(meta_no_match) + Fore.RESET + "/" + str(count))
    print("== end summary == ")
    print("")


if __name__ == '__main__':
    debug('./tests/corpus/')