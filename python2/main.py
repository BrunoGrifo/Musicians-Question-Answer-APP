#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Main script for DBpedia quepy.
"""

import sys
import time
import random
import datetime

import quepy
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
dbpedia = quepy.install("dbpedia")

# quepy.set_loglevel("DEBUG")


def print_define(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        if result[target]["xml:lang"] == "en":
            print result[target]["value"]
            print


def print_enum(results, target, metadata=None):
    used_labels = []

    for result in results["results"]["bindings"]:
        if result[target]["type"] == u"literal":
            if result[target]["xml:lang"] == "en":
                label = result[target]["value"]
                if label not in used_labels:
                    used_labels.append(label)
                    print label


def print_literal(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        literal = result[target]["value"]
        if metadata:
            print metadata.format(literal)
        else:
            print literal


def print_age(results, target, metadata=None):
    assert len(results["results"]["bindings"]) == 1

    birth_date = results["results"]["bindings"][0][target]["value"]
    year, month, days = birth_date.split("-")

    birth_date = datetime.date(int(year), int(month), int(days))

    now = datetime.datetime.utcnow()
    now = now.date()

    age = now - birth_date
    print "{} years old".format(age.days / 365)



if __name__ == "__main__":
   
    if "-d" in sys.argv:
        quepy.set_loglevel("DEBUG")
        sys.argv.remove("-d")

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        questions = [question]
    else:
        print quepy.nltktagger.run_nltktagger(u"List all musics performed by Michael Jackson", nltk_data_path=None)
        print("You have to give me a question my dude!")
        sys.exit()

    print_handlers = {
        "define": print_define,
        "enum": print_enum,
        "literal": print_literal,
        "age": print_age,
    }

    for question in questions:
        print question
        print "-" * len(question)
        target, query, metadata = dbpedia.get_query(question)
        print query
        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None


        #print("-------------------------------------------------"+query_type)
        if query is None:
            print "Query not generated :(\n"
            continue

        if target.startswith("?"):
            target = target[1:]
        if query:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            f = open("output.txt",'w')
            print >>f, results
            

            if not results["results"]["bindings"]:
                print "No answer found :("
                continue
        #print(results)
        """
        print("--------------------------------------------------Entrou")
        print(metadata[0])
        print("---------")
        print(metadata[1])
        print("---------")
        #print(metadata)
        print("--------------------------------------------------Entrou2")
        """
        print_handlers[query_type](results, target, metadata)
        print
