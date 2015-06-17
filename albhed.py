#! /usr/bin/env python3

######################################################################
# This program is free software. It comes without any warranty, to   #
# the extent permitted by applicable law. You can redistribute it    #
# and/or modify it under the terms of the Do What The Fuck You Want  #
# To Public License, Version 2, as published by Sam Hocevar. See     #
# http://www.wtfpl.net/ for more details.                            #
######################################################################

from argparse import ArgumentParser, REMAINDER
from fileinput import input as fileinput
from string import ascii_letters

class AlBhedParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument("-l", "--lang", choices=["spiran", "al_bhed"],
                          help="select the language to translate into", default="al_bhed")
        self.add_argument("-d", "--delimiters", nargs=2, type=str, metavar=("start", "end"),
                          help="set delimiters for proper nouns", default=("\"[", "\"]"))
        self.add_argument("-r", "--remove", type=str, metavar="rm",
                          help="characters to delete in output", default="[]")
        self.add_argument("-t", "--traditional", "--only-canon", action="store_true",
                          help="disable translation of non-canon symbols")

        self.add_argument("file", nargs=REMAINDER)

class AlBhedTrans(object):

    def __init__(self, begin="\"[", end="\"]", rm="[]", just_canon=False):
        self.begin = begin
        self.end = end

        al_bheds = ["y", "p", "l", "t", "a", "v", "k", "r", "e", "z", "g", "m", "s",
                    "h", "u", "b", "x", "n", "c", "d", "i", "j", "f", "q", "o", "w"]

        al_bheds += [a.upper() for a in al_bheds]

        al_bhed = {ascii_letters[i]: al_bheds[i] for i in range(len(ascii_letters))}

        # non canon additions
        if not just_canon:
            al_bhed.update({"ä": "ÿ", "ë": "ä", "ï": "ë", "ö": "ü", "ü": "ï", "ÿ": "ö",
                            "ß": "ç", "ç": "ß"})

        spiran = {al_bhed[key]: key for key in al_bhed.keys()}

        if(any([letter in begin or letter in end or letter in rm for letter in al_bhed.keys()])):
            raise ValueError("Cannot remove letters from input alphabet!")

        spiran.update({s: None for s in rm})
        al_bhed.update({s: None for s in rm})

        self.spiran = str.maketrans(spiran)
        self.al_bhed = str.maketrans(al_bhed)

        self.skip = False

    def translate(self, text, dct):
        ret = ""
        tl = ""
        ntl = ""
        spos = 0
        for i in range(len(text)):
            if not self.skip:
                pos = self.begin.find(text[i])
                if pos >= 0:
                    spos = pos
                    tl += text[i]
                    ret += tl.translate(dct)
                    tl = ""
                    self.skip = True
                else:
                    tl += text[i]
            else:
                pos = self.end.find(text[i])
                if pos == spos:
                    ret += ntl
                    tl += text[i]
                    ntl = ""
                    self.skip = False
                else:
                    ntl += text[i]

        ret += ntl if self.skip else tl.translate(dct)
        return ret

    toAlBhed = lambda self, text: self.translate(text, self.al_bhed)
    toSpiran = lambda self, text: self.translate(text, self.spiran)

args = AlBhedParser().parse_args()
AlBhed = AlBhedTrans(args.delimiters[0], args.delimiters[1], args.remove, args.traditional)

dct = AlBhed.al_bhed if args.lang == "al_bhed" else AlBhed.spiran

for line in fileinput(args.file):
    print(AlBhed.translate(line, dct), end="")
