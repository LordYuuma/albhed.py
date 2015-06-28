from argparse import ArgumentParser, REMAINDER
from collections import Iterable
from re import escape, sub

class ArgumentHelper(ArgumentParser):

    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument("-a", "--al-bhed", nargs=2, type=str, metavar=("start", "end"),
                          help="translate to Al Bhed", default=("\"[", "\"]"))
        self.add_argument("-d", "--delimiters", nargs=2, type=str, metavar=("start", "end"),
                          help="set delimiters for proper nouns", default=("\"[", "\"]"))
        self.add_argument("-n", "--nouns", help="detect proper nouns from file")
        self.add_argument("-r", "--remove", type=str, metavar="rm",
                          help="characters to delete in output", default="[]")
        self.add_argument("-s", "--spiran", action="store_true",
                          help="translate to spiran")
        self.add_argument("-t", "--traditional", "--only-canon", action="store_true",
                          help="disable translation of non-canon symbols")

        self.add_argument("file", nargs=REMAINDER)

    @staticmethod
    def getTranslateWay(translator, args, default="toSpiran"):
        if self.al_bhed and not self.spiran:
            return translator.toAlBhed
        elif self.spiran and not self.al_bhed:
            return translator.toSpiran
        else:
            return getattr(translator, default)

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
            self += nouns

    @staticmethod
    def fromFile(filename):
        dtctr = ProperNounDetector()
        dtctr.addFromFile(filename)
        return dtctr

    def detect(self, text):
        return sub('|'.join(escape(noun) for noun in self.nouns), lambda noun: self.begin + noun.group(0) + self.end, text)
