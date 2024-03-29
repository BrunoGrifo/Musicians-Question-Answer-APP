#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.

# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>


#Save quepy files
#/Users/brunogrifo/opt/anaconda3/envs/conda-env/lib/python2.7/site-packages/quepy/save
"""
Main script for DBpedia quepy.
"""

import sys
import time
import random
import datetime
import pandas as pd
import nltk

import quepy
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
dbpedia = quepy.install("dbpedia")

# quepy.set_loglevel("DEBUG")

#Aproveitado do Quepy
def print_define(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        if result[target]["xml:lang"] == "en":
            try:
                print result[target]["value"]
            except:
                print 

#Aproveitado do Quepy
def print_enum(results, target, metadata=None):
    used_labels = []
    for result in results["results"]["bindings"]:
        if result[target]["type"] == u"literal":
            if result[target]["xml:lang"] == "en":
                label = result[target]["value"]
                if label not in used_labels:
                    used_labels.append(label)
                    try:
                        print label
                    except:
                        print "*****Encoding error*****"


def print_musics(results, target, metadata=None):
    used_labels = []
    for result in results["results"]["bindings"]:
        label = result[target]["value"]
        if label not in used_labels:
            used_labels.append(label)
            try:
                print label
            except:
                print "*****Encoding error*****"

#Aproveitado do Quepy   
def print_literal(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        literal = result[target]["value"]
        if metadata:
            try:
                print metadata.format(literal)
            except:
                print "*****Encoding error*****"
        else:
            try:
                print literal
            except:
                print "*****Encoding error*****"

def print_period(results, target, metadata=None):
    c=True
    entries = target.replace("?","").split(" ")
    for target in entries:
        for result in results["results"]["bindings"]:
            if result[target]["type"] == u"typed-literal":
                if(c):
                    label = result[target]["value"]
                    c=False
                else:
                    label = label +" - " + result[target]["value"]
    print(label)



def print_musicAlbum(results, target, metadata=None):
    music = []
    album = []
    f = open("output.txt",'w')
    entries = target.replace("?","").split(" ")
    for target in entries:
        for result in results["results"]["bindings"]:
            if result[target]["type"] == u"uri":
                label = result[target]["value"]
                music.append(label.replace("-","").split("/")[-1])
                # try:
                #     print label
                # except:
                #     print "*****Encoding error*****"
            if result[target]["type"] == u"typed-literal":
                label = result[target]["value"]
                music.append(label.replace("-",""))
                # try:
                #     print label
                # except:
                #     print "*****Encoding error*****"
            
            if result[target]["type"] == u"literal":
                label = result[target]["value"]
                album.append(label.replace("-",""))
                # try:
                #     print label
                # except:
                #    print "*****Encoding error*****"
    data = {"Album":album,"Music":music}
    df = pd.DataFrame(data)
    df = df.reindex(columns=["Music","Album"])
    print >> f, df.to_string().encode('utf-8')
    print(df.to_string().encode('utf-8'))
    #print(df)

if __name__ == "__main__":
   
    if "-d" in sys.argv:
        quepy.set_loglevel("DEBUG")
        sys.argv.remove("-d")

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        questions = [question]
    else:
        print quepy.nltktagger.run_nltktagger(u"tell me about Steven Tyler", nltk_data_path=None)
        #print("You have to give me a question my dude!")
        # groucho_grammar = nltk.CFG.fromstring("""
        # S -> NP VP
        # PP -> P NP
        # NP -> Det N | Det N PP | 'I'
        # VP -> V NP | VP PP
        # Det -> 'an' | 'my'
        # N -> 'elephant' | 'pajamas'
        # V -> 'shot'
        # P -> 'in'
        # """)
        # sent = ['What', 'are', 'the', 'musics', 'of', 'the', 'album', 'Looking', 'Back', 'to', 'Yesterday']
        # parser = nltk.ChartParser(groucho_grammar)
        # for tree in parser.parse(sent):
        #     print(tree)
        sys.exit()

    print_handlers = {
        "define": print_define,
        "enum": print_enum,
        "literal": print_literal,
        "musics": print_musics,
        "MA": print_musicAlbum,
        "period": print_period,
    }

    for question in questions:
        print question
        print "-" * len(question)
        target, query, metadata = dbpedia.get_query(question)
        #print query
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
