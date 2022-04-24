from tika import parser
import os
import re

#parsed = tika_input
#intro = etracted_intro

def body_extractor(parsed,intro):

    text = parsed["content"]

    lengthintro = len(intro)-30
    intro = intro[lengthintro:]

    print(intro)

    endIntroFinder = text.find(intro)

    print(endIntroFinder)

    text = text[endIntroFinder:]
    #print(text)

    bodystr = ""

    #finding the conclusion Body
    conclusionFinder = text.upper().find('CONCLUSION\n')
    if conclusionFinder == -1:
        conclusionFinder = text.upper().find('RESULT\n')
        if conclusionFinder == -1:
            conclusionFinder = text.upper().find('DISCUSSION\n')

    print(conclusionFinder)
    #cut the conclusion from the text
    text = text[:conclusionFinder]

    split = text.split('\n\n')

    for x in split:
        if len(x)>6:
            bodystr = bodystr + x + '\n\n'
    
    split = bodystr.split('\n\n')
    bodystr = ""

    for x in split:
        if len(x)>1 and x[0].isalnum():
            bodystr = bodystr + x + '\n\n'
    split = bodystr.split('\n\n')
    bodystr = ""

    for x in split:
        if len(x) > 1 and x[0].islower():
            x = ""
        bodystr = bodystr + x + '\n\n'


    return bodystr

    
                

    

fichier.write(body_extractor(parsed).encode())

fichier.close()

