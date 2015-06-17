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
from string import ascii_letters, ascii_lowercase

class AlBhedParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument("-l", "--lang", choices=["spiran", "al_bhed"],
                          help="select the language to translate into", default="al_bhed")

        self.add_argument("file", nargs=REMAINDER)

class AlBhedTrans(object):

    def __init__(self, begin="\"[", end="\"]", rm = "[]"):
        self.begin = begin
        self.end = end

        spirans = ["e", "p", "s", "t", "i", "w", "k", "n", "u", "v", "g", "c", "l",
                   "r", "y", "b", "x", "h", "m", "d", "o", "f", "z", "q", "a", "j"]

        spirans += [s.upper() for s in spirans]

        al_bheds = ["y", "p", "l", "t", "a", "v", "k", "r", "e", "z", "g", "m", "s",
                    "h", "u", "b", "x", "n", "c", "d", "i", "j", "f", "q", "o", "w"]

        al_bheds += [a.upper() for a in al_bheds]

        spiran = {ascii_letters[i]: spirans[i] for i in range(len(ascii_letters))}
        al_bhed = {ascii_letters[i]: al_bheds[i] for i in range(len(ascii_letters))}

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

AlBhed = AlBhedTrans()
args = AlBhedParser().parse_args()

dct = AlBhed.al_bhed if args.lang == "al_bhed" else AlBhed.spiran

for line in fileinput(args.file):
    print(AlBhed.translate(line, dct), end="")
