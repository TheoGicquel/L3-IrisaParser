import json
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span, DocBin

import pprint

read_json = "test3.json"

nlp = spacy.blank("en")
matcher = Matcher(nlp.vocab)



with open(read_json,'r') as f:
    data = json.load(f)

pattern = [[{"TEXT": data["author"][0]["name"]}]]

matcher.add('AUTEUR', pattern)


docs = []
for doc in nlp.pipe(data):
    matches = matcher(doc)
    spans = [Span(doc, start, end, label=match_id) for match_id, start, end in matches]
    doc.ents = spans
    docs.append(doc)

print(docs)


doc_bin = DocBin(docs=docs)
doc_bin.to_disk("./dev.spacy")