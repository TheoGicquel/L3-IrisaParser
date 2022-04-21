from turtle import pos
from pyparsing import line
from tika import parser as tp
import re
# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    filepath = "./tests/corpus_large/Torres.pdf"
    parsed = tp.from_file(filepath)
# ---------------------------------------------------------- #
    
# 'Conclusions and Future Work' 'conclusion' 'conclusion and perspectives' 'conclusion and future work' 'Discussion' '  
# after ACKNOWLEDGEMENT 'ACKNOWLEDGEMENTS' 'REFERENCES' 'APPENDIX *' 'Follow-Up'
endKeywords = ['ACKNOWLEDGMENT','ACKNOWLEDGEMENTS','REFERENCES','APPENDIX','FOLLOW-UP']


def getConclusion(parsed):
    keywords = ['CONCLUSION','RESULT']
    content = parsed["content"]
    res = []
    resultText = []
    lines = content.split('\n\n') # hopefully separate paragraphs
    
    for k in keywords:
        # manage priorities of keywords (i.e Conclusion > Result)
        if(len(res)>0):
            break
        for index,l in enumerate(lines):
            posConc = l[0:15].upper().find(k)
            if(posConc > -1):
                print("found :'"+l+"' at pos:" + str(index) )
                res.append(index+1) # we assume next paragraph is conclusion body
    
    
    lastMatch = res[-1] # use farthest match in document
    print(lastMatch)
    conclusionBody=lines[lastMatch]
    print(conclusionBody)
    
    


# ---------- TEST ONLY (remove before production )---------- #
if __name__ == "__main__":
    res = getConclusion(parsed)
# ---------------------------------------------------------- #
