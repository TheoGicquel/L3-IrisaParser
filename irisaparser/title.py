from ast import For
from cgitb import reset
import pdfplumber
import json
import os
import colorama
from colorama import init,Fore,Back,Style
init() #initialize colorama 


def extract(input_path):
    """
    Attempt to extract title from pdf file using pdfplumber and various methods
    """
    with pdfplumber.open(input_path) as pdf:
        meta_title = extract_from_metadata(pdf)
        first_line = extract_first_line(pdf)
    return meta_title,first_line

def extract_from_metadata(plumbed: pdfplumber.PDF):
    """Returns 'Title' attribute from pdf metadata"""
    output_upper = plumbed.metadata.get('Title')
    output_lower = plumbed.metadata.get('title')
    if(output_upper is not None):
        return output_upper
    if(output_lower is not None):
        return output_lower
    if(output_lower == None and output_lower == None):
        return '!NOT_FOUND!'
        
        

def extract_first_line(plumbed: pdfplumber.PDF):
    """ Fetch first line of pdf file using builtin pdfplumber extract_text() method"""
    title_page_chars = plumbed.pages[0] # only first page used
    filtered = title_page_chars.extract_text(x_tolerance=3, y_tolerance=3, layout=False, x_density=7.25, y_density=13)
    return(filtered.split('\n')[0])
    
def debug(directory):
    errcount = 0
    count = 0
    difcount =0
    print('')
    print("[RUNNING irisaparser.title.debug()]")
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            count = count + 1
            title_meta,title_line = extract(f)
            if(title_meta == '!NOT_FOUND!' or title_meta==''):
                print('['+ str(count) + ']\t' + Fore.BLUE + 'meta : ' + Fore.RED + 'N/A' + Fore.BLUE + '\t\t\t' + 'line : '+ Fore.GREEN + title_line + Fore.RESET)
                errcount = errcount + 1
            else:    
                print('['+ str(count) + ']\t' + Fore.BLUE + 'meta : ' + Fore.GREEN + title_meta + Fore.BLUE + '\t\t\t' + 'line : ' + Fore.GREEN + title_line + Fore.RESET )
            
            if(title_line!=title_meta):
                difcount = difcount + 1


    print("== summary == ")
    print("total pdf files \t\t: " + Fore.YELLOW + str(count) + Fore.RESET)
    print("w/o title metadata \t\t: " + Fore.RED + str(errcount) + Fore.RESET + "/" + str(count))
    print("w/o matching metadata & title \t: " + Fore.RED +  str(difcount) + Fore.RESET + "/" + str(count))
    print("== end summary == ")
    print("")


if __name__ == '__main__':
    debug('./tests/corpus/')