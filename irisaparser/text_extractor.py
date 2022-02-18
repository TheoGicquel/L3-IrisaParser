import pdfplumber
import json
import os
import colorama
from colorama import init,Fore,Back,Style
init() #initialize colorama 
import io # needed for unicode support
encoding='utf-8'
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

    filtered = title_page.filter(lambda x: x.get("size", 0) > 13)
    print(filtered.extract_text())



    return output


def get_largest_font_size(plumbed: pdfplumber.PDF):
    title_page_chars = plumbed.pages[0].chars # only first page used
    largest_font = 0.0
    cur = 0.0
    for i in title_page_chars:
        if(i['size'] > largest_font):
            largest_font = i['size']
            cur = largest_font
    return largest_font   
"""
!TODO: Fix false positives for pdf with larger capital letter than first title
Hypothesis:
    * if font size decreases, then title has been passed
    * extract first 2-3 lines as raw text and compare with best matches of large font size strings
    
    * use lambda function to filter out all chars with size < x (?)
    
    
    
""" 
###############################################################################
    
def extract_dir(in_directory,out_directory):
    """ Attempt title extraction of titles of all pdf files in specified directory

    Args:
        directory (string): path to directory containing pdf files
    """
    meta_missing = 0 # count of files without metadata
    count = 0 # count of pdf files processed
    meta_no_match = 0 # amount of titles not matching with metadata
    lenght = 50 # max lenght of title to display
    tab = '\t' # tab for formatting
    disp_meta = False
    disp_line = False
    print('')
    print("[RUNNING irisaparser.text.extractor]")
    input_paths = os.listdir(in_directory)
    output_paths = os.listdir(out_directory)
    for filename in input_paths:
        filein = os.path.join(in_directory, filename)

        if os.path.isfile(filein):
            with pdfplumber.open(filein) as pdf:
                title_page=pdf.pages[0]
                #print(title_page.objects)
                # x_tolerance : 
                title_page_text=title_page.extract_text(x_tolerance=1,y_tolerance=3).split('\n')
                print(Fore.YELLOW + '[FILE '+ filename + ']' + Fore.RESET)
                itera = 0
                for line in title_page_text[0:3]:
                    itera=itera+1
                    print(Fore.BLUE + 'Line ' + str(itera) + ':'+ Fore.RESET + line)
                #print(type(title_page_text))

                
            






if __name__ == '__main__':
    extract_dir('./tests/corpus/','./tests/single_extracted/')