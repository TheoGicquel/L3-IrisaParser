
if __name__ == "__main__":
    import pdfplumber as plumb
    import tika.parser as tp
   
    
# --------------------------------------------------------- #

# 'Conclusions and Future Work' 'conclusion' 'conclusion and perspectives' 'conclusion and future work' 'Discussion' '  
# after ACKNOWLEDGEMENT 'ACKNOWLEDGEMENTS' 'REFERENCES' 'APPENDIX *' 'Follow-Up'
keywords = ['CONCLUSION','RESULT']
endKeywords = ['ACKNOWLEDGMENT','ACKNOWLEDGEMENTS','REFERENCES','APPENDIX','FOLLOW-UP']



def getConclusionSequences(file):
    '''find lines with matching keywords and return list of positions'''
    content = file["content"]
    keywords_conclusion = ['CONCLUSION','CONCLUSIONS','RESULTS','CONCLUSIONS AND FUTURE WORK','CONCLUSION AND PERSPECTIVES','CONCLUSIONS']

    conclBegPos = None
    conclEndPos = None
    sequences = []
    begSectionPos = []
    print("begin")
    for l in keywords_conclusion:
        conclBegPos = content.upper().find(l)

       
        
        # if((conclBegPos not None) and (conclBegPos not -1)):
        if(conclBegPos>0):
            # try to find end of line in next 30 characters 
            conclEndPos = content[conclBegPos:conclBegPos+35].upper().find('\n')
           
            if(conclEndPos>0):
                 # since array was resized during search, fix indexing
                conclEndPos+=conclBegPos
                sequences.append([conclBegPos,conclEndPos])
                begSectionPos.append(conclEndPos)
                print('l:',end='')
                print(l,end='   ')
                print(conclEndPos)
                
        
    begSectionPos.sort(reverse=True)
    print("end")

    endSectionPos = []
    for l in endKeywords:
        endsection = content.upper().find(l)

        if(endsection>0):
            print('l:',end='')
            print(l,end='   ')
            print(endsection)
            endSectionPos.append(endsection)
    
    endSectionPos.sort(reverse=True)
    print(begSectionPos)
    
    print(endSectionPos)
    
    print("attempt : ",end='')
    
    
    beginSection = begSectionPos[0]
    endSection = endSectionPos[0]
    
    print("["+ str(beginSection) + "," + str(endSection) + "]")

    print(content[beginSection:endSection])
    
                
    for seq in sequences:
        pass
        #print(content[seq[0]:endsection])
    if(len(sequences)>0):
        return sequences
    else:
        return None




def getConclusion(filePath):
    # find conclusion begin posistions
    tikaparsed = tp.from_file(filePath)
    conclSeq = getConclusionSequences(tikaparsed)
    return None
    if(conclSeq is None):
        return None
    
    content = tikaparsed["content"]
    
    
    
    # test positions with pdfplumber
    pdf = plumb.open(filePath)
    
    plumbedConclLines = []
    
    for l in conclSeq:
        beginC = l[0]
        endC = l[1]
        
        print(l,end="(len:")
        print(endC-beginC,end=")\n")
        plumbedConclLines.append(pdf.chars[beginC:endC])
        
    for line in plumbedConclLines:
        for char in line:
            print(char['text'],end='')
        print("")

    #remainder = remainder.replace('-\n','') # replace newlines for words splits
    #remainder = remainder
    #remainder = remainder.split('\n')
    return None

# ---------- DEV ONLY (remove before production )---------- #
print(getConclusion("./tests/corpus_large/Torres.pdf"))
# --------------------------------------------------------- #
