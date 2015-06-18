from collections import Iterable
from re import escape, sub

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

    def detect(self, text):
        return sub('|'.join(escape(noun) for noun in self.nouns), lambda noun: self.begin + noun.group(0) + self.end, text)
