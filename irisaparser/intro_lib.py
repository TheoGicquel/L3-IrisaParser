# -*- coding: utf-8 -*-

# from tika import parser  
# import os
import re



def intro_extractor(parsed):


    data = parsed['content'] 


    intro = re.search(r"\n(1|I).+(Introduction|INTRODUCTION)\n", data, re.I).group()


    end = re.search(r"\n(2|II).+[a-zA-Z]+(\s[a-zA-Z]+).\n", data, re.I).group()

    integer = data.find(intro)

    content = data[integer+len(intro):data.find(end)]

    split = content.split('\n\n')

    finalstr = ""


    for x in split:
        if x.startswith('http') or x.startswith('\t') or x.startswith('\n\t') or x.startswith('∗'):
                x = " "
        if len(x) > 50:
            if x[0].islower(): 
                finalstr += "\n" + str(x)
            else :
                finalstr += "\n\n" + str(x)

 
    return finalstr[2:]






























