from tika import parser
import os

pdf = []


parsed = parser.from_file('btp709.pdf')

fichier = open("text.txt", "wb")

listPdf = [x for x in os.listdir("./") if x.endswith(".pdf")]

#print(listPdf)

def reference_extractor(parsed):
    texte = parsed["content"]
    texte = texte[1000:]
    reference_finder = texte.find('\nReferences')

# find references location in the texte
    if reference_finder == -1:
        reference_finder = texte.find('\nREFERENCES')

        if reference_finder == -1:
            return "there are no references in this file"
        
    #print(reference_finder)

    
    texte = texte[reference_finder + 10:]

    split = texte.split('\n\n')

    finalstr = ""
    

    for x in split:
        if x.startswith('http') | x.startswith('\t') | x.startswith('\n\t'):
                x = " "
        if len(x) > 10:
            if x[0].islower(): #if the first character of a paragraph is not uppercase stick it to the end of the paragraph above
                finalstr += "\n" + str(x)
            elif x.find(',') == -1:
                x = ""
            else :
                finalstr += "\n\n" + str(x)

    return finalstr[2:]

 
fichier.write(reference_extractor(parsed).encode())

fichier.close()