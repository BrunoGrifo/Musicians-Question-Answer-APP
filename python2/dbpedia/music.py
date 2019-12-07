# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Music related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsBand, LabelOf, IsMemberOf, ActiveYears, MusicGenreOf, \
    NameOf, IsAlbum, ProducedBy, DefinitionOf, IsPerson, BirthPlaceOf, ParentOf, ChildOf, GenreOf


class Band(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return HasKeyword(name)


class BandMembersQuestion(QuestionTemplate):

    """
    Regex for questions about band member.
    Ex: "Radiohead members"
        "What are the members of Metallica?"
    """

    regex1 = Band() + Lemma("member")
    regex2 = Lemma("member") + Pos("IN") + Band()
    regex3 = Pos("WP") + Lemma("be") + Pos("DT") + Lemma("member") + \
        Pos("IN") + Band()

    regex = (regex1 | regex2 | regex3) + Question(Pos("."))

    def interpret(self, match):
        member = IsMemberOf(match.band)
        label = LabelOf(member)
        return label, "enum"


class FoundationQuestion(QuestionTemplate):
    """
    Regex for questions about the creation of a band.
    Ex: "When was Pink Floyd founded?"
        "When was Korn formed?"
    """

    regex = Pos("WRB") + Lemma("be") + Band() + \
        (Lemma("form") | Lemma("found")) + Question(Pos("."))

    def interpret(self, match):
        active_years = ActiveYears(match.band)
        return active_years, "literal"


class GenreQuestion(QuestionTemplate):
    """
    Regex for questions about the genre of a band.
    Ex: "What is the music genre of Gorillaz?"
        "Music genre of Radiohead"
    """

    optional_opening = Question(Pos("WP") + Lemma("be") + Pos("DT"))
    regex = optional_opening + Question(Lemma("music")) + Lemma("genre") + \
        Pos("IN") + Band() + Question(Pos("."))

    def interpret(self, match):
        genre = MusicGenreOf(match.band)
        label = LabelOf(genre)
        return label, "enum"


class AlbumsOfQuestion(QuestionTemplate):
    """
    Ex: "List albums of Pink Floyd"
        "What albums did Pearl Jam record?"
        "Albums by Metallica"
    """

    regex = (Question(Lemma("list")) + (Lemma("album") | Lemma("albums")) + \
             Pos("IN") + Band()) | \
            (Lemmas("what album do") + Band() +
             (Lemma("record") | Lemma("make")) + Question(Pos("."))) | \
            (Lemma("list") + Band() + Lemma("album"))

    def interpret(self, match):
        album = IsAlbum() + ProducedBy(match.band)
        name = NameOf(album)
        return name, "enum"


class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)


class WhoIs(QuestionTemplate):
    """
    Ex: "Who is Tom Cruise?"
    """
    regex = Lemma("who") + Lemma("be") + Person() + Question(Pos("."))

    def interpret(self, match):
        definition = DefinitionOf(match.person)
        return definition, "define"



class WhereIsFromQuestion(QuestionTemplate):
    """
    Ex: "Where is Bill Gates from?"
    """

    regex = Lemmas("where be") + Person() + Lemma("from") + \
        Question(Pos("."))

    def interpret(self, match):
        birth_place = BirthPlaceOf(match.person)
        label = LabelOf(birth_place)

        return label, "enum"

class ParentsOf(QuestionTemplate):
    """
    Ex: "Who are Liv Tyler parents?"
    """
    regex1 = Lemmas("who be") + Person() + Lemma("parent") + Question(Pos("."))
    regex2 = Lemmas("who be") + Person() + (Pos("POS") + Pos("NN")) + Lemma("parent") + Question(Pos("."))
    regex = regex1 | regex2

    def interpret(self, match):
        parent = ParentOf(match.person)
        label = LabelOf(parent)
        return label, "define"


class ChildrenOf(QuestionTemplate):
    """
    Ex: "Who are the sons of Steven Tyler?"
    """
    regex = Lemmas("who be") + Pos("DT") + (Lemma("son") | Lemma("child")) + Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        child = ChildOf(match.person)
        label = LabelOf(child)
        return label, "define"

class GenreOf(QuestionTemplate):
    """
    Ex: What are the music genres of Michael Jackson?
    """
    regex = (Lemmas("who be") | Lemma("list")) + Pos("DT") + (Lemmas("music genre") | Lemma("genre")) + Pos("IN") +\
            Person() + Question(Pos("."))

    def interpret(self, match):
        genre= GenreOf(match.person)
        label = LabelOf(genre)
        return label, "enum"