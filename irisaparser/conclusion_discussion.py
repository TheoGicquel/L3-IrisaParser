import pdfplumber
import re
# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    filepath = "./tests/corpus_large/Torres.pdf"
    pdf = pdfplumber.open(filepath)
# ---------------------------------------------------------- #
    
# 'Conclusions and Future Work' 'conclusion' 'conclusion and perspectives' 'conclusion and future work' 'Discussion' '  
# after ACKNOWLEDGEMENT 'ACKNOWLEDGEMENTS' 'REFERENCES' 'APPENDIX *' 'Follow-Up'
keywords = ['CONCLUSION','RESULT']
endKeywords = ['ACKNOWLEDGMENT','ACKNOWLEDGEMENTS','REFERENCES','APPENDIX','FOLLOW-UP']




def getConclusion(pdf:pdfplumber.PDF):
    # REMINDER : pdf.chars is a list of dict
    alltext = []
    pagesCharNum =[]
    
    for p in pdf.pages:
        pagesCharNum.append(len(p.chars))

    
    conclPos = []
    
    
    for p in pdf.pages:
        text = p.extract_text(x_tolerance=3, y_tolerance=3)

        keyword = "CONCLUSION"
        keywordB = "RESULT"
        pos = text.upper().find(keyword)
        if(pos>0):
            print("found at pos : "+str(pos) + "@p " + str(p.page_number-1))
            conclPos.append(pos)
            #conclPos.append(pos+pagesCharNum[p.page_number-1])
        else:
            pos = text.upper().find(keywordB)
            if(pos>0):
                print("found at pos : "+str(pos) + "@p " + str(p.page_number-1))
                conclPos.append(pos)
                #conclPos.append(pos+pagesCharNum[p.page_number-1])
            
    
    for pos in conclPos:
        seq = pdf.chars[pos:pos+30]
        print("\n--- match --")
        for char in seq:
            print(char['text'],end='')
            

    #text = pdf.extract_text(x_tolerance=3, y_tolerance=3)
    
        # Remove unecessary chars
        #text = re.sub("a´","à",text)
        #text = re.sub("´e","é",text)
        #text = re.sub("e´","è",text)
        #text = re.sub("c¸","ç",text)
        #text = re.sub("ˆı","î",text)
    



# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    res = getConclusion(pdf)
    print(res)
# ---------------------------------------------------------- #
