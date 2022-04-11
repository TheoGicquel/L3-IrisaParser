

if __name__ == "__main__":
    import pdfplumber
    import tika.parser as tp
    parsed = tp.from_file("./tests/corpus/single/Boudin-Torres-2006.pdf")
    
# --------------------------------------------------------- #

# 'Conclusions and Future Work' 'conclusion' 'conclusion and perspectives' 'conclusion and future work' 'Discussion' '  
# after ACKNOWLEDGEMENT 'ACKNOWLEDGEMENTS' 'REFERENCES' 'APPENDIX *' '7 Follow-Up Work'
keywords = ['CONCLUSION','RESULTS']

    
def getConclusionPosition(file):
    content = file["content"]
    keywords_conclusion = ['CONCLUSION','CONCLUSIONS','RESULTS','CONCLUSIONS AND FUTURE WORK','CONCLUSION AND PERSPECTIVES','CONCLUSIONS']

    conclBegPos = None
    for l in keywords_conclusion:
        conclBegPos = content.upper().find(l)
        if(conclBegPos!=None and conclBegPos !='-1'):
            print(conclBegPos)




def getConclusion(filePath):
    content = parsed["content"]
    conclBegPos = content.upper().find('DISCUSSION AND FUTURE WORK')
    remainder = content[conclBegPos:]
    remainder = remainder.replace('-\n','') # replace newlines for words splits
    remainder = remainder
    #remainder = remainder.split('\n')
    return remainder

# ---------- DEV ONLY (remove before production )---------- #
print(getConclusionPosition(parsed))
# --------------------------------------------------------- #
