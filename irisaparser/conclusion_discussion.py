from tika import parser as tp
# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    filepath = "./tests/corpus_large/Torres.pdf"
    parsed = tp.from_file(filepath)
# ---------------------------------------------------------- #
    
# 'Conclusions and Future Work' 'conclusion' 'conclusion and perspectives' 'conclusion and future work' 'Discussion' '  
# after ACKNOWLEDGEMENT 'ACKNOWLEDGEMENTS' 'REFERENCES' 'APPENDIX *' 'Follow-Up'
debug = False
def dprint(input):
    if(debug):
        print(input)

def getConclusion(parsed):
    endKeywords = ['ACKNOWLEDGMENT','ACKNOWLEDGEMENTS','REFERENCES','APPENDIX','FOLLOW-UP']
    beginKeywords = ['CONCLUSION','RESULT']
    content = parsed["content"]
    resBegin = []
    resEnd = []
    resultText = []
    lines = content.split('\n\n') # hopefully separate paragraphs
    
    for k in beginKeywords:
        # manage priorities of keywords (i.e Conclusion > Result)
        if(len(resBegin)>0):
            break
        for index,l in enumerate(lines):
            posConc = l[0:15].upper().find(k)
            if(posConc > -1):
                dprint("found :'"+l+"' at pos:" + str(index) )
                resBegin.append(index+1) # we assume next paragraph is conclusion body
    
    BeginArea = resBegin[-1] # use farthest match in document
    for k in endKeywords:
        if(len(resEnd)>0): # break loop at first 
            break
        for index,l in enumerate(lines):
            posNextParagraph = l[0:15].upper().find(k)
            if(posNextParagraph > -1):
                dprint("found :'"+l+"' at pos:" + str(index) )
                resEnd.append(index) # we assume next paragraph is conclusion body
    EndArea = resEnd[-1]
    dprint("--- endarea----")
    dprint(lines[EndArea])
    dprint("---------------")
    
    dprint("result: begin at line [" + str(BeginArea) + '] ends at [' + str(EndArea) + "]")
    endArray = lines[BeginArea:EndArea]
    final = ''
    for l in endArray:
        final = f'{final}{l}'
    return final
    
    


# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    res = getConclusion(parsed)
    print(res)
# ---------------------------------------------------------- #
