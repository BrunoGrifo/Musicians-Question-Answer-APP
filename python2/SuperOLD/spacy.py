from __future__ import unicode_literals
import spacy
import sys
from spacy import displacy

STYLE = ""

def image(style,doc):
    #ent e dep
    displacy.serve(doc, style=style)


def instructions():
    print("----------Tags----------")
    print("PRON - " + spacy.explain("PRON"))
    print("AUX - " + spacy.explain("AUX"))
    print("PROPN - " + spacy.explain("PROPN"))
    print("ADP - " + spacy.explain("ADP"))
    print("PUNCT - " + spacy.explain("PUNCT"))
    print("NOUN - " + spacy.explain("NOUN"))
    print("VERB - " + spacy.explain("VERB"))
    print("------------------------")

def tokenizer():
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load("en_core_web_sm")
    quest = "What was the day Micheal Jackosn died?"
    doc = nlp(quest)

    # Analyze syntax
    for token in doc:
        print(token.text +" - "+ token.tag_ +" - "+ token.pos_ +" - "+token.dep_+" - "+token.lemma_)

    print("Noun phrases:", [token.text for token in doc.noun_chunks])
    print("Verbs:", [token.text for token in doc if token.pos_ == "VERB"])
    print("Entities:", [token.text for token in doc.ents])
    print("Stop words:", [token.text for token in doc if token.is_stop==True])

    #Image
    if STYLE:
        image(STYLE,doc)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("To much dude!")
        sys.exit()
    if len(sys.argv) == 2:
        STYLE = sys.argv[1]
    instructions()
    tokenizer()