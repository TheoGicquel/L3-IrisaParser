import pdfplumber as pp
import sys
import os
from tika import parser 


corpusPath = "../Corpus_2021"

output_file = open("output.txt", "wb")

file = os.path.join(corpusPath,"Nasr.pdf")

parsed = parser.from_file(file)  

#with pp.open(file) as pdf:
#    first_page = pdf.pages[0]
#
#    text = first_page.extract_text(y_tolerance=0.5)


#print(type(text))
#output_file.write(text.encode())
#output_file.close()
#
#test_file = open("test.txt", "wb")
#
#print(len(first_page.chars))
#print(first_page.chars[0].keys())

#for index,obj in enumerate(first_page.chars):
#    test_line = str("> "+obj['text']+"("+str(obj['x0'])+","+str(obj['y0'])+")->("+str(obj['x1'])+","+str(obj['y1'])+")\n")
#    test_file.write(test_line.encode('utf-8'))
#    print(index)
#    if(index == 5): break

file.write(parsed["content"].encode())


test_file.close()
