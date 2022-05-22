# -*- coding: utf-8 -*-

from posixpath import abspath


def abstract_extractor(parsed):
    abstr = parsed["content"].upper().find('ABSTRACT')
    intro = parsed["content"].upper().find('INTRODUCTION')
    if intro == -1:
        intro = parsed["content"].upper().find('I N T R O D U C T I O N')
    end = len(parsed["content"])

    text = parsed["content"]

    if abstr == -1: # abstract not found
        splited_text = text[:intro].split("\n\n")

        for x in splited_text:
            if len(x) > 200:
                return x
        return "error"

    else:
        cut = 0
        for x in range(intro, abstr, -1):
            if text[x] == "\n" and text[x-1] == "\n":
                cut = x
                break
    
        return text[abstr+8:cut] if end-intro > 6000 else text[abstr+8:cut].split("\n\n")[0]
