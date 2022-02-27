def abstract_extractor(parsed):
    abstr = parsed["content"].upper().find('ABSTRACT')
    intro = parsed["content"].upper().find('INTRODUCTION')

    print(abstr)
    print(intro)

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
        
        for index,t in enumerate(text[abstr+8:cut].split("\n\n")): print("index: "+str(index)+"\n"+t)

        return text[abstr+8:cut].split("\n\n")[0]