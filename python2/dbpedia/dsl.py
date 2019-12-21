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
#HasKeyword.relation = "rdfs:label"
HasKeyword.relation = "foaf:name"
HasKeyword.language = "en"



class IsPerson(FixedType):
    fixedtype = "foaf:Person"


class IsBand(FixedType):
    fixedtype = "dbpedia-owl:Band"

class IsAlbum(FixedType):
    fixedtype = "dbpedia-owl:Album"


class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True

class GenreOf(FixedRelation):
    relation = "dbpedia-owl:genre"
    reverse = True

class LabelOf(FixedRelation):
    relation = "foaf:name"
    reverse = True

class IsMemberOf(FixedRelation):
    relation = "dbpedia-owl:bandMember"
    reverse = True


class ActiveYears(FixedRelation):
    relation = "dbpedia-owl:activeYearsStartYear"
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

class NameOf(FixedRelation):
    relation = "foaf:name"
    reverse = True




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

class ActivityPeriodEndOf(FixedRelation):
    relation = "dbpedia-owl:activeYearsEndYear"
    reverse = True

class ActivityPeriodStartOf(FixedRelation):
    relation = "dbpedia-owl:activeYearsStartYear"
    reverse = True

class CauseDeathOf(FixedRelation):
    relation = "dbpedia-owl:deathCause"
    reverse = True

class CauseDeathName(FixedRelation):
    relation = "rdfs:label"
    reverse = True

class DayDeathOf(FixedRelation):
    relation = "dbpedia-owl:deathYear"
    reverse = True

class TitleOf(FixedRelation):
    relation = "dbpedia-owl:title"
    reverse = True

class ArtistOf(FixedRelation):
    relation = "dbpedia-owl:artist"
    reverse = False

class AlbumTitleOf(FixedRelation):
    relation = "foaf:name"
    reverse = True

class MusicTitleOf(FixedRelation):
    relation = "dbp:title"
    reverse = True