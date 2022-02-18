import pdfplumber
import json
# Work in progress, do not use

def get_largest_font_size(plumbed: pdfplumber.PDF):
    title_page_chars = plumbed.pages[0].chars # only first page used
    largest_font = 0.0
    for i in title_page_chars:
        if(i['size'] > largest_font):
            largest_font = i['size']
    return largest_font    


def extract(input_path):
    """ Dummy function"""
    pdf = pdfplumber.open(input_path)
    # convert pdf to json
    title_page_chars = pdf.pages[0].chars

    
    # determine average largest font size
    charcount = 0
    sum_font_size=0
    precision = 1
    

    largest_font = get_largest_font_size(pdf)
    
    output = ''
    for i in title_page_chars:
        if (i['size'] - largest_font < precision) and (i['size'] - largest_font > -precision):
            output+=str(i['text'])

    print(output)
    return output
        
    
        

out = extract('./tests/corpus/Boudin-Torres-2006.pdf')
#print(extract('./tests/custom/test_minimal.pdf'))
#print(out)




