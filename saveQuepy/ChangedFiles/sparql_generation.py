# -*- coding: utf-8 -*-

"""
Sparql generation code.
"""
import sys

from quepy import settings
from quepy.dsl import IsRelatedTo
from quepy.expression import isnode
from quepy.encodingpolicy import assert_valid_encoding

_indent = u"  "


def escape(string):
    string = unicode(string)
    string = string.replace("\n", "")
    string = string.replace("\r", "")
    string = string.replace("\t", "")
    string = string.replace("\x0b", "")
    if not string or any([x for x in string if 0 < ord(x) < 31]) or \
            string.startswith(":") or string.endswith(":"):
        message = "Unable to generate sparql: invalid nodes or relation"
        raise ValueError(message)
    return string


def adapt(x):
    if isnode(x):
        x = u"?x{}".format(x)
        return x
    if isinstance(x, basestring):
        assert_valid_encoding(x)
        
        if x.startswith(u"\"") or ":" in x:
            return x
        return u'"{}"'.formt(x)
    return unicode(x)


def expression_to_sparql(e, full):
    template = u"{preamble}\n" +\
               u"SELECT DISTINCT {select} WHERE {{\n" +\
               u"{expression}\n" +\
               u"}}\n"
    select= adapt(e[0].get_head())
    if full:
        for x in range(1,len(e)):
            select += " " + adapt(e[x].get_head()+x)

    y = 0
    xs = []
    count=0
    xCount = 0
    for x in e:
        for node in x.iter_nodes():
            for relation, dest in x.iter_edges(node):
                if(count<3):
                    if relation is IsRelatedTo:
                        relation = u"?y{}".format(y)
                        xs.append("1")
                        print("Entrou")
                        y += 1
                    if ((type(dest) is int) and (len(e)>1)):
                        xs.append(triple(adapt(node), relation, adapt(dest+xCount),indentation=1))
                        #xs.append("2 - " + dest.__str__() + count.__str__())
                        count+=1
                        if(dest!=0):
                            xCount+=1
                    else:
                        xs.append(triple(adapt(node), relation, adapt(dest),indentation=1))
                        #xs.append("3 - " + dest.__str__() )

    sparql = template.format(preamble=settings.SPARQL_PREAMBLE,
                             select=select,
                             expression=u"\n".join(xs))
                    
    #sys.exit(1)
    return select, sparql


def triple(a, p, b, indentation=0):
    a = escape(a)
    b = escape(b)
    p = escape(p)
    s = _indent * indentation + u"{0} {1} {2}."
    return s.format(a, p, b)