from tika import parser  

import os
import re

parsed_pdf = parser.from_file("./PDF/Gonzalez_2018_Wisebe.pdf")



data = parsed_pdf['content'] 

noPage = re.findall('\n\n[0-9]+\n\n', data)


fichier = open("./TXTTest/Gonzalez_2018_Wisebe.txt", "wb")




intro = re.search(r"\n(1|I).+(Introduction|INTRODUCTION)\n", data, re.I).group()


end = re.search(r"\n(2|II).+[a-zA-Z]+(\s[a-zA-Z]+).\n", data, re.I).group()

integer = data.find(intro)

content = data[integer+len(intro):data.find(end)]

# enlever les numeros de pages 
j = 0
for i in noPage:
    if i in content:
        while j < len(noPage):
            if j == 0:
                content = re.sub(noPage[j],"",content)
            tmp = content
            content = re.sub(noPage[j],"",tmp)
            j += 1

fichier.write(content.encode())

fichier.close()


























