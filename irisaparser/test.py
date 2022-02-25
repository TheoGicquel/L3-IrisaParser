import pdfplumber as pp
import sys
import os
from tika import parser 


corpusPath = "../Corpus_2021"

output_file = open("output.txt", "wb")

file = os.path.join(corpusPath,"Nasr.pdf")

parsed = parser.from_file(file)  

listPdf = [x for x in os.listdir("./") if x.endswith(".pdf")]

print(listPdf)

def abstract_extractor(parsed):
    abstr = parsed["content"].upper().find('ABSTRACT')
    intro = parsed["content"].upper().find('INTRODUCTION')

    text = parsed["content"]

    text.format()

    if abstr == -1:
        splitedText = text[:intro].split("\n\n")

        for x in splitedText:
            if len(x) > 150:
                return x
        return "error"
                
        

    else:
        cut = 0
        for x in range(intro, abs, -1):

            if text[x] == "\n" and text[x-1] == "\n":
                cut = x
                break
        return text[abs:cut]

    

output_file.write(abstract_extractor(parsed).encode())

output_file.close()
