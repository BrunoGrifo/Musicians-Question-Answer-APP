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
    InstrumentOf, OccupationOf, BirthDateOf, ActivityPeriodEndOf, ActivityPeriodStartOf, CauseDeathOf, DayDeathOf, TitleOf, CauseDeathName, ArtistOf, AlbumTitleOf, MusicTitleOf


#-------------------------------PARTICLES--------------------------------------------------------------------


class Band(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))
    #regex = Question(Pos("DT")) +  Pos("NNP")

    def interpret(self, match):
        name = match.words.tokens.title()
        #print(name)
        name = name.replace("List ","")
        name = name.replace(" list","")
        return HasKeyword(name)


class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        name = name.replace(" music","")
        #print(name)
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
        "What was the foundation year of Pink Floyd?"  
        "In what year was Pink Floyd founded?"
    """

    regex1 = Pos("WRB") + Lemma("be") + Band() + (Lemma("form") | Lemma("found")) + Question(Pos("."))
    regex2 = Lemmas("what be") + Pos("DT") + Lemmas("foundation year") + Pos("IN") + Band() + Question(Pos(".")) ############################################
    regex3 = Lemmas("in what year be") + Band() + Lemma("found") + Question(Pos(".")) ############################################################

    regex = regex1 | regex2 | regex3
    def interpret(self, match):
        active_years = ActiveYears(match.band)
        return [active_years], "literal"

class AlbumsOfQuestion(QuestionTemplate): #--------------------------------DONE
    """
    Ex: "List albums of Pink Floyd"
        "What albums did Pearl Jam record?"
        "Albums by Metallica"
        "What albuns do Pearl Jam have?"
    """

    regex1 = Question(Lemma("list")) + (Lemma("album") | Lemma("albums")) + Pos("IN") + Band() + Question(Pos("."))
    regex2 = Lemma("what") + (Lemma("album") | Lemma("albums")) + Lemma("do") + Band() + Lemma("record") + Question(Pos("."))
    regex3 = Question(Lemma("list")) + (Lemma("album") | Lemma("albums")) + Pos("IN") + Band() + Question(Pos("."))
    regex4 = Lemma("what") + (Lemma("albuns") | Lemma("album")) + Lemma("do") + Band() + Lemma("have") + Question(Pos("."))
    regex = regex1 | regex2 | regex3 | regex4
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
        "Where did Bill Gates came from?"
    """

    regex1 = Lemmas("where be") + Person() + (Lemma("from") | Lemma("bear")) + Question(Pos("."))
    regex2 = Lemmas("where do") + Person() + Lemmas("come from") + Question(Pos(".")) #####################################################
    regex = regex1 | regex2

    def interpret(self, match):
        birth_place = BirthPlaceOf(match.person)
        label = LabelOf(birth_place)

        return [label], "enum"


class ParentsOf(QuestionTemplate): #-----------------------------------DONE
    """
    Ex: "Who are Liv Tyler parents?"
        "Who are Liv Tyler's parents?"
        "Who are parents of Liv Tyler?"
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
    Ex: Who are the sons/girls of Steven Tyler?
        Who are Steven Tyler's children?
        List Steven Tyler's children
    """
    regex1 = Lemmas("who be") + Person() + Question((Pos("POS") + Pos("NN"))) + (
                Lemma("son") | Lemma("child") | Lemma("girl")) + Question(Pos("."))
    regex2 = Lemmas("who be") + Pos("DT") + (Lemma("son") | Lemma("child") | Lemma("girl")) + Pos("IN") + Person() + Question(Pos("."))
    regex3 = Lemma("list") + Person()+ Question((Pos("POS") + Pos("NN"))) + Lemma("child")
    regex = regex1 | regex2 | regex3

    def interpret(self, match):
        child = ChildOf(match.person)
        label = LabelOf(child)
        return [label], "define"

class GenresOf(QuestionTemplate):  # --------------------------- DONE
    """
    Ex: What are the music genres of Michael Jackson?
        List Micheal Jackson music genres
        List the muric genres of Michael Jackson
        What genres do Michael Jackson play?
        
    """
    regex1 = Lemmas("what be") + Pos("DT") + (Lemmas("music genre") | Lemma("genre")) + Pos("IN") + Person() + Question(Pos("."))
    regex2 = Lemma("list")  +  Person() + (Lemmas("music genre") | Lemma("genre")) + Question(Pos("."))
    regex3 = Lemma("list")  + Pos("DT") + (Lemmas("music genre") | Lemma("genre")) + Pos("IN") +  Person()
    regex4 = Question(Pos("WP") + Lemma("be") + Pos("DT"))
    regex5 = regex4 + Question(Lemma("music")) + Lemma("genre") + Pos("IN") + Band() + Question(Pos("."))
    regex6 = Lemmas("what genres do") + Person() + Lemma("play") + Question(Pos(".")) 
    regex = regex1 | regex2 | regex3 | regex4 | regex5 | regex6
    def interpret(self, match):
        genre= GenreOf(match.person)
        label = LabelOf(genre)
        return [label], "enum"

class BirthNamesOf(QuestionTemplate): #------------------------DONE
    """
    Ex: What is the real name of Eminem?
        What is Eminem's real name?
        what is Eminem's birth name?
        what is the birth name of Eminem?
    """
    regex1 = Lemmas("what be") + Pos("DT") + (Lemmas("real name") | Lemmas("birth name")) + Pos("IN") + Person() + Question(Pos("."))
    regex2 = Lemmas("what be") + Person() + Question(Pos("POS") + Pos("JJ")) + (Lemmas("real name") | Lemmas("birth name")) + Question(Pos("."))
    regex = regex1 | regex2
    def interpret(self, match):
        birth = BirthNameOf(match.person)
        return [birth], "define"

class InstrumentsOf(QuestionTemplate): #-------------------------DONE
    """
    Ex: What instruments does Dave Grohl play? 
        List the instruments that Dave Grohl plays    ------------------------why?
        What are the instruments that Dave Grohl is known for?



    """
    regex1 = (Lemma("what") | Lemma("which")) + Lemma("instrument") + Question(Lemma("do")) + Person() + Lemma("play") + Question(Pos("."))
    regex2 = Lemma("list") + Pos("DT") + Lemma("instrument") + Pos("WDT") + Person() + Lemma("play") + Question(Pos("."))
    regex3 = Lemmas("what be") + Pos("DT") + Lemma("instrument") + Pos("WDT") + Person() + Lemma("be") + Lemma("know") + Lemma("for") + Question(Pos("."))
    regex = regex1 | regex2 | regex3

    def interpret(self, match):
        instrument = InstrumentOf(match.person)
        return [instrument],"literal"

class OccupationsOf(QuestionTemplate): #--------------------DONE 
    """
    Ex: What are the occupations of Jennifer Lopez?
        What does Jennifer Lopez do?
        What are Jennifer Lopez other jobs?
        What does Jennifer Lopez do besides <verb>?
        What is Jennifer Lopez profession?
        What does Jennifer Lopez do for living?
        What is Jennifer Lopez known for?
        What are Jennifer Lopez's occupations?
        List Jennifer Lopez occupations
        List Jennifer Lopez other jobs
        List Jennifer Lopez professions
    """
    regex1 = Lemmas("what be") + Pos("DT") + Lemma("occupation") + Pos("IN") + Person() + Question(Pos("."))
    regex2 = Lemmas("what do") + Person() + Lemma("do") + Question(Pos("IN") + (Pos("NN") | Pos("VBG") | Pos("VB"))) + Question(Pos("."))
    regex3 = Lemmas("what be") + Person()
    regex4 = regex3 + (Question(Lemma("other")) + Lemma("job") | Lemma("profession") | Lemma("know") + Pos("IN"))+ Question(Pos("."))
    regex7 = regex3 + Pos("POS") + Pos("NN") + (Lemma("profession") | (Question(Lemma("other")) + Lemma("job")) | Lemma("occupation")) + Question(Pos("."))
    regex8 = Lemma("list") + Person() + (Lemma("profession") | (Question(Lemma("other")) + Lemma("job")) | Lemma("occupation")) + Question(Pos("."))
    
    
    regex = regex1 | regex2 | regex4 | regex7 | regex8

    def interpret(self, match):
        occupation = OccupationOf(match.person)
        title = TitleOf(occupation)
        return [title], "literal"

class BirthDatesOf(QuestionTemplate):  #------------------------Done
    """
    Ex: When was Justin Bieber born?
        When was the day Justin Bieber was born?

    """
    regex1 = Lemmas("when be") + Question(Pos("DT") + Lemma("day")) + Person() + Question(Lemma("be")) + Lemma("bear") + Question(Pos("."))
    regex = regex1

    def interpret(self, match):
        birthdate = BirthDateOf(match.person)
        return [birthdate],"literal"

class ActivityPeriodsOf(QuestionTemplate): 
    """
    Ex: What is the activity period of Amy Winehouse?
        In what years 
        Active years of 
    """
    regex = Lemmas("what be") + Pos("DT") + Lemmas("activity period") + Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        
        periodEnd = ActivityPeriodEndOf(match.person)
        periodStart = ActivityPeriodStartOf(match.person)
        #period = [periodStart,periodEnd]
        return [ActivityPeriodStartOf(match.person), ActivityPeriodEndOf(match.person)], "period"

class CauseDeathsOf(QuestionTemplate): #-----------------------DONE
    """
    Ex: What was the cause of death of Amy Winehouse?
        How did Amy Winehouse die?
    """
    regex1 = Lemmas("what be") + Pos("DT") + Lemma("cause") + Pos("IN") + Lemma("death") + Pos("IN") + Person() + Question(Pos("."))
    regex2 = Lemmas("how do") + Person() + Lemma("die") + Question(Pos("."))
    regex = regex1 | regex2

    def interpret(self, match):
        causedeath = CauseDeathOf(match.person)
        name = CauseDeathName(causedeath)
        return [name], "literal"

class DayDeathsOf(QuestionTemplate): #-----------------------------DONE +-
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


class AlbumsOf(QuestionTemplate): #-----------------Done
    """
    Ex: List all Michael Jackson's albums
        List all albums performed by Michael Jackson
        List all albums of Michael Jackson
        what are the albums of Michael Jackson

    """
    regex1 = Lemma("list") + Question(Lemma("all")) + (Person() | Band()) + Question(Pos("POS") + Pos("NN")) + Lemma("album") + Question(Pos("."))
    regex2 = Lemma("list") + Question(Lemma("all")) + Lemma("album") + Question(Lemma("perform")) + Pos("IN") + (Person() | Band()) + Question(Pos("."))
    regex3 = Lemmas("what be") + Pos("DT") + Lemma("album") + Pos("IN") + Person() + Question(Pos("."))
    regex = regex1 | regex2 | regex3
    def interpret(self, match):
        artist = ArtistOf(match.person)
        albums = AlbumTitleOf(artist)
        return [albums],"enum"


# class MusicsOf(QuestionTemplate): 
#     """
#     Ex: List all Michael Jackson's musics
#         List all musics performed by Michael Jackson
#         What are the musics of Michael Jackson

#     """
#     regex1 = Lemma("list") + Question(Lemma("all")) + (Person() | Band()) +  Question(Pos("POS") + Pos("NN"))  + Lemma("music") + Question(Pos("."))
#     regex2 = Lemma("list") + Question(Lemma("all")) + Lemma("music") + Question(Lemma("perform")) + Pos("IN") + (Person() | Band()) + Question(Pos("."))
#     regex3 = Lemmas("what be") + Pos("DT") + Lemma("music") + Pos("IN") + Person() + Question(Pos("."))
#     regex = regex1 | regex2 | regex3
#     def interpret(self, match):
#         artist = ArtistOf(match.person)
#         musics = MusicTitleOf(artist)

#         return [musics],"musics"


class MusicsOf(QuestionTemplate): 
    """
    Ex: List all Michael Jackson's musics
        List all musics performed by Michael Jackson
        What are the musics of Michael Jackson

    """
    regex1 = Lemma("list") + Question(Lemma("all")) + (Person() | Band()) +  Question(Pos("POS") + Pos("NN"))  + Lemma("music") + Question(Pos("."))
    regex2 = Lemma("list") + Question(Lemma("all")) + Lemma("music") + Question(Lemma("perform")) + Pos("IN") + (Person() | Band()) + Question(Pos("."))
    regex3 = Lemmas("what be") + Pos("DT") + Lemma("music") + Pos("IN") + Person() + Question(Pos("."))
    regex = regex1 | regex2 | regex3
    def interpret(self, match):
        artist = ArtistOf(match.person)
        musics = MusicTitleOf(artist)
        albums = AlbumTitleOf(artist)
        return [musics, albums],"MA"


class Album(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS") | Pos("VB") | Pos("DT") | \
            Pos("VBG") | Pos("CC") | Pos("IN") | Pos("CD") | Pos("PRP") | Pos("POS") | Pos(".") | \
            Pos("TO") | Pos("JJ") | Pos("JJS")| Pos(":") | Pos(")") | Pos("("))

    def interpret(self, match):
        name = match.words.tokens
        if((name[-1]==".") | (name[-1]=="?")):
            name = name[:-2]
        name = name.replace(" ?","")
        name = name.replace("?","")
        print(name)
        return HasKeyword(name)

class MusicOfAlbum(QuestionTemplate): 
    """
    Ex: List all music of Looking Back to Yesterday
        What are the musics of Looking Back to Yesterday
        What musics compose Looking Back to Yesterday
    """
    regex1 = Lemma("list") + Question(Lemma("all")) + Lemma("music") + Pos("IN") + Album() + Question(Pos("."))
    regex2 = Lemmas("what be") + Pos("DT") + Lemma("music") + Pos("IN") + Album() + Question(Pos("."))
    regex3 = Lemma("what") + Lemma("musics") + Lemma("compose") + Album() + Question(Pos("."))
    regex = regex1 | regex2 | regex3
    def interpret(self, match):
        print(match.__str__())
        album = match.album + IsAlbum()
        musics = MusicTitleOf(album)
        return [musics],"musics"
