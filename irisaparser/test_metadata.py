import lib_metadata
mypdf = "../corpus/Boudin-Torres-2006.pdf"

current_metadata = lib_metadata.extract(mypdf)
#print(current_metadata)
print(current_metadata['Title'])