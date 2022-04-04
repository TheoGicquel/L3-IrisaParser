# ---------- DEV ONLY (remove before production )---------- #
if __name__ == "__main__":
    from tika import parser as tp
    parsed = tp.from_file("./tests/corpus/single/Boudin-Torres-2006.pdf")
# --------------------------------------------------------- #

# 'Conclusions and Future Work' 'conclusion' 'conclusion and perspectives' 'conclusion and future work' 'Discussion' ' 

keywords = ['CONCLUSION','RESULTS']


def getConclusion(parsed):

    concl = parsed["content"].upper().find('CONCLUSION')
    return concl

# ---------- DEV ONLY (remove before production )---------- #
print(getConclusion(parsed))
# --------------------------------------------------------- #