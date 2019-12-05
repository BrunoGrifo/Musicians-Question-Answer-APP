# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
People related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import  LabelOf, BirthDateOf, BirthPlaceOf

"""
class Person(Particle):
    print("--------------------------------------------------Person Particle")
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)





class HowOldIsQuestion(QuestionTemplate):

    How old is Bob Dylan


    regex = Pos("WRB") + Lemma("old") + Lemma("be") + Person() + 
        Question(Pos("."))

    def interpret(self, match):
        birth_date = BirthDateOf(match.person)
        return birth_date, "age"



"""