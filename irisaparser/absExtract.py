import os
from tika import parser 


corpusPath = "../../test/Corpus_2021"

output_file = open("output.txt", "wb")

file = os.path.join(corpusPath,"Nasr.pdf")

parsed = parser.from_file(file)  

def abstract_extractor(parsed):
    abstr = parsed["content"].upper().find('ABSTRACT')
    intro = parsed["content"].upper().find('INTRODUCTION')

    # print(intro)
    # print(abstr)

    text = parsed["content"]

    # print(text)

    if abstr == -1:
        splited_text = text[:intro].split("\n\n")

        for x in splited_text:
            if len(x) > 150:
                return x
        return "error"

    else:
        cut = 0
        for x in range(intro, abstr, -1):
            if text[x] == "\n" and text[x-1] == "\n":
                cut = x
                break
        print(text[abstr:cut])
        return text[abstr+8:cut]

    

output_file.write(abstract_extractor(parsed).encode())

output_file.close()
