import re

pdf = []

parsed = parser.from_file("./PDF/On_the_Morality_of_Artificial_Intelligence.pdf")

fichier = open("./TXTTest/On_the_Morality_of_Artificial_Intelligence.txt", "wb")

listPdf = [x for x in os.listdir("./") if x.endswith(".pdf")]

def intro_extractor(parsed):

    

    data = parsed['content'] 

    intro = "1 I n t r o d u c t i o n" #jing
    intro2 = "1 Introduction" #iria
    intro3 = "1. Introduction" #survey 
    intro4 = "1 Artificial Intelligence Leaves the Research Lab"


    if intro2 in data:
        tmp = intro2
        intro2 = intro
        intro = tmp

    elif intro3 in data:
        tmp = intro3
        intro3 = intro
        intro = tmp    
    elif intro4 in data:
        data = " "
        return data
    elif not intro in  data:
        intro = re.search(r"\n(1|I).+(Introduction|INTRODUCTION)\n", data, re.I).group()
    

    

    end = "2. Description of some terminology extraction systems " #survey

    if not end in data:
        end = re.search(r"\n(2|II).[^0]+([a-zA-Z]+(\s[a-zA-Z]+).).\n", data, re.I).group()

        
    integer = data.find(intro)

    content = data[integer+len(intro):data.find(end)]


    split = content.split('\n\n')

    finalstr = ""


    for x in split:
        if x.startswith('http') or x.startswith('\t') or x.startswith('\n\t') or x.startswith('∗')  or x.endswith('.org'):
                x = " "
        if len(x) > 50:
            if x[0].islower(): 
                finalstr += "\n" + str(x)
            else :
                finalstr += "\n\n" + str(x)
    return finalstr[2:]
































