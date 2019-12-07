# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Domain specific language for DBpedia quepy.
"""

from quepy.dsl import FixedType, HasKeyword, FixedRelation, FixedDataRelation

# Setup the Keywords for this application
HasKeyword.relation = "rdfs:label"
HasKeyword.language = "en"



class IsPerson(FixedType):
    fixedtype = "foaf:Person"


# class IsPlace(FixedType):
#     fixedtype = "dbpedia:Place"


# class IsCountry(FixedType):
#     fixedtype = "dbpedia-owl:Country"


class IsBand(FixedType):
    fixedtype = "dbpedia-owl:Band"


class IsAlbum(FixedType):
    fixedtype = "dbpedia-owl:Album"


# class HasName(FixedDataRelation):
#     relation = "dbpprop:name"
#     language = "en"


class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True


class LabelOf(FixedRelation):
    relation = "rdfs:label"
    reverse = True




# class LanguageOf(FixedRelation):
#     relation = "dbpprop:officialLanguages"
#     reverse = True



class IsMemberOf(FixedRelation):
    relation = "dbpedia-owl:bandMember"
    reverse = True


class ActiveYears(FixedRelation):
    relation = "dbpprop:yearsActive"
    reverse = True


class MusicGenreOf(FixedRelation):
    relation = "dbpedia-owl:genre"
    reverse = True


class ProducedBy(FixedRelation):
    relation = "dbpedia-owl:producer"



class BirthDateOf(FixedRelation):
    relation = "dbpprop:birthDate"
    reverse = True


class BirthPlaceOf(FixedRelation):
    relation = "dbpedia-owl:birthPlace"
    reverse = True


# class ReleaseDateOf(FixedRelation):
#     relation = "dbpedia-owl:releaseDate"
#     reverse = True


# class ShowNameOf(FixedRelation):
#     relation = "dbpprop:showName"
#     reverse = True


# class HasActor(FixedRelation):
#     relation = "dbpprop:starring"


# class CreatorOf(FixedRelation):
#     relation = "dbpprop:creator"
#     reverse = True


class NameOf(FixedRelation):
    relation = "foaf:name"
    # relation = "dbpprop:name"
    reverse = True


# class DirectedBy(FixedRelation):
#     relation = "dbpedia-owl:director"


# class DirectorOf(FixedRelation):
#     relation = "dbpedia-owl:director"
#     reverse = True


# class HasAuthor(FixedRelation):
#     relation = "dbpedia-owl:author"


# class AuthorOf(FixedRelation):
#     relation = "dbpedia-owl:author"
#     reverse = True




# class LocationOf(FixedRelation):
#     relation = "dbpedia-owl:location"
#     reverse = True


class ParentOf(FixedRelation):
    relation = "dbpedia-owl:parent"
    reverse = True

class ChildOf(FixedRelation):
    relation = "dbpedia-owl:child"
    reverse = True

class GenreOf(FixedRelation):
    relation = "dbpedia-owl:genre"
    reverse = True

class BirthNameOf(FixedRelation):
    relation = "dbpedia-owl:birthName"
    reverse = True

class InstrumentOf(FixedRelation):
    relation = "dbpprop:instrument"
    reverse = True

class OccupationOf(FixedRelation):
    relation = "dbpedia-owl:occupation"
    reverse = True

class BirthDateOf(FixedRelation):
    relation = "dbpedia-owl:birthDate"
    reverse = True