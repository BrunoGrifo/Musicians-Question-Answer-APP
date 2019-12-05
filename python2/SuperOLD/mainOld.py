import sys
import quepy
import nltk

from SPARQLWrapper import SPARQLWrapper, JSON




sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def sparqlQuery():
    sparql.setQuery("""
        SELECT ?name WHERE {
            ?person rdfs:label "Eminem" @en .
            ?person dbo:birthName ?name
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["name"]["value"])


if __name__ == "__main__":
    #nltk.download()

    question = "What was the cause of death of Amy Winehouse?"

    tokens = nltk.word_tokenize(question)

    tags = nltk.pos_tag(tokens)

    print(tokens)
    print("----------------------")
    print(tags)
    sparqlQuery()