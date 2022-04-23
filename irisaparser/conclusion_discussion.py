from tika import parser as tp
# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    filepath = "./tests/corpus_large/Torres.pdf"
    parsed = tp.from_file(filepath)
# ---------------------------------------------------------- #
    
# 'Conclusions and Future Work' 'conclusion' 'conclusion and perspectives' 'conclusion and future work' 'Discussion' '  
# after ACKNOWLEDGEMENT 'ACKNOWLEDGEMENTS' 'REFERENCES' 'APPENDIX *' 'Follow-Up'

# enable to print debug info to stdout
debug = True
def dprint(input):
    if(debug):
        print(input)

NOT_FOUND_MSG = "NOT FOUND"

def getConclusion(parsed):
    endKeywords = ['ACKNOWLEDGMENT','ACKNOWLEDGEMENTS','REFERENCES','APPENDIX','FOLLOW-UP']
    beginKeywords = ['CONCLUSION','RESULT']
    content = parsed["content"]
    resBegin = []
    resEnd = []
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
    
    if(len(resBegin)==0):
        return NOT_FOUND_MSG
    
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
    
    # append all lines into single string
    final = ''
    for l in endArray:
        final = f'{final}{l}'
    return final
    
def getDiscussion(parsed):
    content = parsed["content"]
    posDisc= []
    lines = content.split('\n\n') # hopefully separate paragraphs
    
    for index,l in enumerate(lines):
            pos = l[0:15].upper().find('DISCUSSION')
            if(pos > -1):
                dprint("found :'"+l+"' at pos:" + str(index) )
                posDisc.append(index+1) # we assume next paragraph is discussion body

    if(len(posDisc)>0):    
        discusArea = posDisc[-1] # use farthest match in document
        return lines[discusArea]
    else:
        return NOT_FOUND_MSG


# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    concl = getConclusion(parsed)
    #print(concl)
    discussion = getDiscussion(parsed)
    print(discussion)
# ---------------------------------------------------------- #
