#! /usr/bin/env python3

######################################################################
# This program is free software. It comes without any warranty, to   #
# the extent permitted by applicable law. You can redistribute it    #
# and/or modify it under the terms of the Do What The Fuck You Want  #
# To Public License, Version 2, as published by Sam Hocevar. See     #
# http://www.wtfpl.net/ for more details.                            #
######################################################################

from fileinput import input as fileinput
from string import ascii_letters, ascii_lowercase

class AlBhedTrans(object):
    spiran = ["e", "p", "s", "t", "i", "w", "k", "n", "u", "v", "g", "c", "l",
              "r", "y", "b", "x", "h", "m", "d", "o", "f", "z", "q", "a", "j"]
    al_bhed = ["y", "p", "l", "t", "a", "v", "k", "r", "e", "z", "g", "m", "s",
               "h", "u", "b", "x", "n", "c", "d", "i", "j", "f", "q", "o", "w"]

    def __init__(self, begin=[], end=[]):
        self.begin = begin
        self.end = end

        self.skip = False

    def translate(self, text, dct):
        ret = ""
        tl = ""
        ntl = ""
        for i in range(len(text)):
            if not self.skip:
                if text in self.begin:
                    ret += _translate(tl, dct)
                    tl = ""
                    self.skip = True
                else:
                    tl += text[i]
            else:
                if text in self.end:
                    ret += ntl
                    ntl = ""
                    self.skip = False
                else:
                    ntl += text[i]

        ret += ntl if self.skip else self._translate(tl, dct)
        return ret


    def _translate(self, text, dct):
        ret = ""
        for i in range(len(text)):
            char = text[i]
            if char not in ascii_letters:
                ret += char
            elif char in ascii_lowercase:
                ret += dct[ord(char)-ord("a")]
            else:
                ret += chr(ord("A") + ord(dct[ord(char)-ord("A")]) - ord("a"))
        return ret

    toAlBhed = lambda self, text: self.translate(text, self.al_bhed)
    toSpiran = lambda self, text: self.translate(text, self.spiran)


AlBhed = AlBhedTrans(["\"", "["], ["]", "\""])

for line in fileinput():
    print(AlBhed.toAlBhed(line))
