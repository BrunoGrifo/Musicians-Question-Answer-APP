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
    NameOf, IsAlbum, ProducedBy, DefinitionOf, IsPerson, BirthPlaceOf, ParentOf, ChildOf, GenreOf, BirthNameOf, \
    InstrumentOf, OccupationOf, BirthDateOf, ActivityPeriodEndOf, ActivityPeriodStartOf, CauseDeathOf, DayDeathOf


#-------------------------------PARTICLES--------------------------------------------------------------------


class Band(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))
    #regex = Question(Pos("DT")) +  Pos("NNP")

    def interpret(self, match):
        name = match.words.tokens.title()
        name = name.replace("List ","")
        name = name.replace(" list","")
        print(name)
        return HasKeyword(name)


class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        name = name.replace(" music","")
        return HasKeyword(name)


#---------------------------------------------------------------------------------------------------------------------










class BandMembersQuestion(QuestionTemplate): #---------------------DONE

    """
    Regex for questions about band member.
    Ex: "Radiohead members"
        "What are the members of Metallica?"
    """

    regex1 = Band() + Lemma("member")
    regex2 = Lemma("member") + Pos("IN") + Band()
    regex3 = Pos("WP") + Lemma("be") + Pos("DT") + Lemma("member") + \
        Pos("IN") + Band()
    regex4 = Lemma("list") + Pos("DT") + Lemma("member") + Pos("IN") + Band()
    regex5 = Lemma("list") + Band() + Lemma("member")

    regex = (regex1 | regex2 | regex3 | regex4| regex5) + Question(Pos("."))

    def interpret(self, match):
        #.replace("List","")
        member = IsMemberOf(match.band)
        label = LabelOf(member)
        return [label], "enum"


class FoundationQuestion(QuestionTemplate):  #------------------------------DONE
    """
    Regex for questions about the creation of a band.
    Ex: "When was Pink Floyd founded?"
        "When was Korn formed?"
    """

    regex = Pos("WRB") + Lemma("be") + Band() + \
        (Lemma("form") | Lemma("found")) + Question(Pos("."))

    def interpret(self, match):
        active_years = ActiveYears(match.band)
        return [active_years], "literal"

class AlbumsOfQuestion(QuestionTemplate): #--------------------------------DONE
    """
    Ex: "List albums of Pink Floyd"
        "What albums did Pearl Jam record?"
        "Albums by Metallica"
    """

    regex1 = Question(Lemma("list")) + (Lemma("album") | Lemma("albums")) + Pos("IN") + Band() + Question(Pos("."))
    regex2 = Lemma("what") + (Lemma("album") | Lemma("albums")) + Lemma("do") + Band() + Lemma("record") + Question(Pos("."))
    regex3 = Question(Lemma("list")) + (Lemma("album") | Lemma("albums")) + Pos("IN") + Band() + Question(Pos("."))
    regex = regex1 | regex2 | regex3
    def interpret(self, match):
        album = IsAlbum() + ProducedBy(match.band)
        name = NameOf(album)
        return [name], "enum"


class WhoIs(QuestionTemplate):  #-----------------------------Done
    """
    Ex: "Who is Tom Cruise?"
    """
    regex = Lemma("who") + Lemma("be") + Person() + Question(Pos("."))


    def interpret(self, match):
        definition = DefinitionOf(match.person)
        return [definition], "define"


class WhereIsFromQuestion(QuestionTemplate): #-----------------------------DONE
    """
    Ex: "Where is Bill Gates from?"
    Ex: "Where was Whitney Houston born?"
    """

    regex = Lemmas("where be") + Person() + (Lemma("from") | Lemma("bear")) + Question(Pos("."))

    def interpret(self, match):
        birth_place = BirthPlaceOf(match.person)
        label = LabelOf(birth_place)

        return [label], "enum"


class ParentsOf(QuestionTemplate): #-----------------------------------DONE
    """
    Ex: "Who are Liv Tyler parents?"
    """
    regex1 = Lemmas("who be") + Person() + Question((Pos("POS") + Pos("NN"))) + Lemma("parent") + Question(Pos("."))
    regex2 = Lemmas("who be") + Pos("DT") + Lemma("parent") + Pos("IN") + Person() + Question(Pos("."))
    regex = regex1 | regex2

    def interpret(self, match):
        parent = ParentOf(match.person)
        label = LabelOf(parent)
        return [label], "define"


class ChildrenOf(QuestionTemplate): #-----------------------------DONE
    """
    Ex: "Who are the sons of Steven Tyler?"
        "List Steven Tyler children"
    """
    regex1 = Lemmas("who be") + Person() + Question((Pos("POS") + Pos("NN"))) + (
                Lemma("son") | Lemma("child")) + Question(Pos("."))
    regex2 = Lemmas("who be") + Pos("DT") + (Lemma("son") | Lemma("child")) + Pos("IN") + Person() + Question(Pos("."))
    regex3 = Lemma("list") + Person() + Lemma("child")
    regex = regex1 | regex2 | regex3

    def interpret(self, match):
        child = ChildOf(match.person)
        label = LabelOf(child)
        return [label], "define"

class GenresOf(QuestionTemplate):  # --------------------------- DONE
    """
    Ex: What are the music genres of Michael Jackson?
        List Micheal Jackson music genres
        
    """
    regex1 = Lemmas("what be") + Pos("DT") + (Lemmas("music genre") | Lemma("genre")) + Pos("IN") + Person() + Question(Pos("."))
    regex2 = Lemma("list")  +  Person() + (Lemmas("music genre") | Lemma("genre")) + Question(Pos("."))
    regex3 = Lemma("list")  + Pos("DT") + (Lemmas("music genre") | Lemma("genre")) + Pos("IN") +  Person()
    regex4 = Question(Pos("WP") + Lemma("be") + Pos("DT"))
    regex5 = regex4 + Question(Lemma("music")) + Lemma("genre") + Pos("IN") + Band() + Question(Pos("."))
    regex = regex1 | regex2 | regex3 | regex4 | regex5
    def interpret(self, match):
        genre= GenreOf(match.person)
        label = LabelOf(genre)
        return [label], "enum"

class BirthNamesOf(QuestionTemplate):
    """
    Ex: What is the real name of Eminem?
    """
    regex1 = Lemmas("what be") + Pos("DT") + (Lemmas("real name") | Lemmas("birth name")) + Pos("IN") + Person() + Question(Pos("."))
    regex2 = Lemmas("what be") + Person() + Question((Pos("POS") + Pos("NN"))) + (Lemmas("real name") | Lemmas("birth name"))
    regex = regex1 | regex2
    def interpret(self, match):
        birth = BirthNameOf(match.person)
        return [birth], "define"

class InstrumentsOf(QuestionTemplate):
    """
    Ex: What instruments does Dave Grohl play?
    """
    regex = Lemmas("what instrument") + Question(Lemma("do")) + Person() + Lemma("play") + Question(Pos("."))

    def interpret(self, match):
        instrument = InstrumentOf(match.person)
        return [instrument],"literal"

class OccupationsOf(QuestionTemplate):
    """
    Ex: What are the occupations of Jennifer Lopez?
    """
    regex = Lemmas("what be") + Pos("DT") + Lemma("occupation") + Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        occupation = OccupationOf(match.person)
        return [occupation],"literal"

class BirthDatesOf(QuestionTemplate):
    """
    Ex: When was Justin Bieber born?
    """
    regex = Lemmas("when be") + Person() + Lemma("bear") + Question(Pos("."))

    def interpret(self, match):
        birthdate = BirthDateOf(match.person)
        return [birthdate],"literal"

class ActivityPeriodsOf(QuestionTemplate): #----------------------------------O GRIFO FEZ ESTA MAL
    """
    Ex: What is the activity period of Amy Winehouse?
        In what years 
        Active years of 
    """
    regex = Lemmas("what be") + Pos("DT") + Lemmas("activity period") + Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        """
        periodEnd = ActivityPeriodEndOf(match.person)
        periodStart = ActivityPeriodStartOf(match.person)
        period = [periodStart,periodEnd]
        """
        return [ActivityPeriodStartOf(match.person),ActivityPeriodEndOf(match.person)], "literal"

class CauseDeathsOf(QuestionTemplate): #-----------------------O GRIFO FEZ ESTA  MAL
    """
    Ex: What was the cause of death of Amy Winehouse?
    """
    regex = Lemmas("what be") + Pos("DT") + Lemma("cause") + Pos("IN") + Lemma("death") + Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        causedeath = CauseDeathOf(match.person)
        return [causedeath], "literal"

class DayDeathsOf(QuestionTemplate):
    """
    Ex: When did Amy Winehouse died?
    What was the death day of Amy Winehouse?
    What was the day of death of Amy Winehouse?
    In what day did Amy Winehouse died?
    What day did Amy Winehouse died?
    """
    regex1 = Lemmas("when do") + Person() + Lemma("die") + Question(Pos("."))
    regex2 = Lemmas("what be") + Pos("DT") + (Lemmas("death day") | (Lemma("day") + Pos("IN") + Lemma("death"))) + Pos("IN") + Person() + Question(Pos("."))
    regex3 = Pos("IN") + Lemmas("what day do") + Person() + Lemma("die") + Question(Pos("."))
    regex4 = Lemmas("what day do") + Person() + Lemma("die") + Question(Pos("."))
    regex = regex1 | regex2 | regex3 | regex4

    def interpret(self, match):
        daydeath = DayDeathOf(match.person)
        return [daydeath],"literal"