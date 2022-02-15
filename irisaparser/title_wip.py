import pdfplumber
import json
# Work in progress, do not use




def extract(input_path):
    """ Dummy function"""
    pdf = pdfplumber.open(input_path)
    # convert pdf to json
    title_page_chars = pdf.pages[0].chars

    
    # determine average largest font size
    charcount = 0
    sum_font_size=0
    precision = 1
    
    #for i in title_page_chars:
    #    sum_font_size = sum_font_size + round(i['size'],4)
    #    charcount = charcount + 1
    #avg_size = sum_font_size/charcount
    #print(avg_size)
    
    title_page_lines = pdf.pages[0].lines
    print (title_page_lines)
    
    
    largest_font = 0.0
    for i in title_page_chars:
        if(i['size'] > largest_font):
            largest_font = i['size']
            
    print (largest_font)
    
    output = ''
    for i in title_page_chars:
        if (i['size'] - largest_font < precision) and (i['size'] - largest_font > -precision):
            output+=str(i['text'])

    return output
        
    
        

out = extract('./tests/corpus/Boudin-Torres-2006.pdf')
#print(extract('./tests/custom/test_minimal.pdf'))
#print(out)




