# -*- coding: utf-8 -*-

def getConclusion(parsed):
    endKeywords = ['ACKNOWLEDGMENT','ACKNOWLEDGEMENTS','REFERENCES','APPENDIX','FOLLOW-UP']
    beginKeywords = ['CONCLUSION','CONCLUSIONS']
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
                resBegin.append(index+1) # we assume next paragraph is conclusion body
    
    if(len(resBegin)==0):
        return None
    
    BeginArea = resBegin[-1] # use farthest match in document
    for k in endKeywords:
        if(len(resEnd)>0): # break loop at first 
            break
        for index,l in enumerate(lines):
            posNextParagraph = l[0:15].upper().find(k)
            if(posNextParagraph > -1):
                resEnd.append(index) # we assume next paragraph is conclusion body
    

    # no paragraph found
    if(len(resEnd) == 0):
        return None

    
    EndArea = resEnd[-1]
    
    endArray = lines[BeginArea:EndArea]
    
    # append all lines into single string
    final = ''
    for l in endArray:
        final = f'{final}{l}'
    if(len(final)>0):
            return final
    return None
    
def getDiscussion(parsed):
    content = parsed["content"]
    posDisc= []
    lines = content.split('\n\n') # hopefully separate paragraphs
    
    for index,l in enumerate(lines):
            pos = l[0:15].upper().find('DISCUSSION')
            if(pos > -1):              
                posDisc.append(index+1) # we assume next paragraph is discussion body

    if(len(posDisc)>0):    
        discusArea = posDisc[-1] # use farthest match in document
        return lines[discusArea]
    else:
        return None