# import parser object from tike
import string
from tika import parser  
import re
from random import *



# opening pdf file
parsed_pdf = parser.from_file("Das_Martins.pdf")
  
data = parsed_pdf['content'] 
 

references1 = "REFERENCES"
references2 = "References"

if references1 in data:
    integer = data.find(references1)
    reference = data[integer+len(references1):]
    #print(reference)
elif references2 in data:
    integer = data.find(references2)
    reference = data[integer+len(references2):]


    #noPage = reference.find("28") #2247
    #noPage = reference.find("29") #4384

    #indexes = [x.start() for x in re.finditer("28",reference)]
    #print(indexes) # <--[2247, 2263, 4380, 4859, 6552]
    #noPage = indexes[1] # 2263


    indexes = [x.start() for x in re.finditer("29",reference)]
    # print(indexes) # <--[4384, 4602, 7485]
    noPage = indexes[1] # 4602


    # print(reference[4599:4609])










    # string = "\n\n28\n\n\n"

    # if string in reference:
    #     mod_string = re.sub(string,'', reference )
    # print(mod_string)


    #print(noPage)

    if "]"in (reference[reference.rfind("."):-1]) :

        samedi = reference[:reference.rfind("]")+1]

        #print(jeudi)

        #number=["0","1","2","3","4","5","6","7","8","9"]

      
        #tirer =  choice(number)
        # print(reference[:reference.rfind("]")+1])

        x = re.findall('\n\n[0-9]+\n\n', samedi)
    
      
        j = 0
        for i in x:
            if i in samedi:
                while j < len(x):
                    if j == 0:
                        mod_string = re.sub(x[j],"",samedi)
                    tmp = mod_string
                    mod_string = re.sub(x[j],"",tmp)
                    j += 1
        print(mod_string)





        # if l in jeudi:
            #print("yes")
            # mod_string = re.sub(l,"\n",jeudi)
        # print(mod_string)



        #if string in jeudi:
         #   mod_string = re.sub(string,'', jeudi)
        #print(mod_string)

        # print(mod_string)
    # else:
        # print(reference[:reference.rfind(".")+1])
        # string = "\n\n28\n\n\n"

        # if string in reference:
        #     mod_string = re.sub(string,'', reference )
        # print(mod_string)

    




else:
    print('There is no reference.') 

    






