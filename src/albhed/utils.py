######################################################################
# This program is free software. It comes without any warranty, to   #
# the extent permitted by applicable law. You can redistribute it    #
# and/or modify it under the terms of the Do What The Fuck You Want  #
# To Public License, Version 2, as published by Sam Hocevar. See     #
# http://www.wtfpl.net/ for more details.                            #
######################################################################

from argparse import ArgumentParser, REMAINDER
from collections import Iterable
from re import escape, sub


class ArgumentHelper(ArgumentParser):

    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument("-a", "--al-bhed", action="store_true",
                          help="translate to Al Bhed")
        self.add_argument("-d", "--delimiters", nargs=2, type=str,
                          metavar=("start", "end"), default=("\"[", "\"]"),
                          help="set delimiters for proper nouns")
        self.add_argument("-n", "--nouns",
                          help="detect proper nouns from file")
        self.add_argument("-r", "--remove", type=str, metavar="rm",
                          help="characters to delete in output", default="[]")
        self.add_argument("-s", "--spiran", action="store_true",
                          help="translate to spiran")
        self.add_argument("-t", "--traditional", "--only-canon",
                          action="store_true",
                          help="disable translation of non-canon symbols")

        self.add_argument("file", nargs=REMAINDER)

    @staticmethod
    def getTranslateWay(translator, args, default=None):
        if args.al_bhed and not args.spiran:
            return translator.toAlBhed
        elif args.spiran and not args.al_bhed:
            return translator.toSpiran
        else:
            return default


class ASCIIDowngrader(object):

    def __init__(self):
        trans = {"ä": "ae", "ë": "e", "ï": "i", "ö": "oe", "ü": "ue", "ÿ": "y",
                 "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ý": "y",
                 "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u", "ỳ": "y",
                 "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u", "ŷ": "y",
                 "ß": "ss", "ç": "c", "Ç": "C", "ẞ": "SS"}
        self._trans = str.maketrans(trans)

    def downgrade(self, text):
        return text.translate(self._trans)


class ProperNounDetector(object):

    def __init__(self, nouns=[], begin="[", end="]"):
        self.nouns = nouns
        self.begin = begin
        self.end   = end

    def __add__(self, nouns: Iterable):
        if isinstance(nouns, str):
            self.nouns.append(nouns)
        else:
            self.nouns += nouns
        return self

    def addFromFile(self, filename):
        with open(filename) as fin:
            nouns = [line.strip() for line in fin]

            nouns = [noun for noun in nouns
                     if not noun.startswith("#")
                     and not noun.startswith(";")
                     and not noun.startswith("//")]

            self += nouns

    @staticmethod
    def fromFile(filename):
        dtctr = ProperNounDetector()
        dtctr.addFromFile(filename)
        return dtctr

    def detect(self, text):
        return sub('|'.join(escape(noun) for noun in self.nouns),
                   lambda noun: self.begin + noun.group(0) + self.end,
                   text)
