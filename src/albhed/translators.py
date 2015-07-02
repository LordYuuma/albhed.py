######################################################################
# This program is free software. It comes without any warranty, to   #
# the extent permitted by applicable law. You can redistribute it    #
# and/or modify it under the terms of the Do What The Fuck You Want  #
# To Public License, Version 2, as published by Sam Hocevar. See     #
# http://www.wtfpl.net/ for more details.                            #
######################################################################

from . import maps
from .utils import ASCIIDowngrader

class AlBhedTranslator(object):

    def __init__(self, al_bhed_lower, proper_noun_begin, proper_noun_end, tbr):
        self._proper_begin = proper_noun_begin
        self._proper_end   = proper_noun_end

        al_bhed = dict(al_bhed_lower)
        al_bhed.update({a.upper(): al_bhed[a].upper() for a in al_bhed.keys()})
        al_bhed = {a: al_bhed[a] for a in al_bhed.keys() if len(a) == 1 and len(al_bhed[a]) == 1}
        spiran = {al_bhed[key]: key for key in al_bhed.keys()}

        if(any([letter in self._proper_begin or letter in self._proper_end or letter in tbr for letter in al_bhed.keys()])):
            raise ValueError("Cannot remove letters from input alphabet!")

        rm = {r: None for r in tbr}
        al_bhed.update(rm)
        spiran.update(rm)

        self._al_bhed = str.maketrans(al_bhed)
        self._spiran  = str.maketrans(spiran)
        self._remove  = str.maketrans(rm)

        self._markers = []

    def _translate(self, text, dct):
        text = self._prepare(text)

        ret = ""
        tl = ""
        ntl = ""

        for i in range(len(text)):
            if not len(self._markers):
                beg = self._proper_begin.find(text[i])

                if beg >= 0:
                    self._markers += [beg]
                    tl += text[i]
                    ret += tl.translate(dct)
                    tl = ""
                else:
                    tl += text[i]
            else:
                beg = self._proper_begin.find(text[i])
                end = self._proper_end.find(text[i])

                if end == self._markers[-1]:
                    self._markers.pop()
                    ntl += text[i]
                    if len(self._markers) == 0:
                        ret += ntl.translate(self._remove)
                        ntl = ""
                else:
                    if beg >= 0:
                        self._markers += [beg]
                    ntl += text[i]

        ret += ntl.translate(self._remove) if len(self._markers) else tl.translate(dct)
        return ret

    _prepare = lambda self, text: text

    toAlBhed = lambda self, text: self._translate(text, self._al_bhed)
    toSpiran = lambda self, text: self._translate(text, self._spiran)

class RomanCanonTranslator(AlBhedTranslator):

    def __init__(self, begin="\"[", end="\"]", tbr="[]"):
        AlBhedTranslator.__init__(self, maps.canon["roman"], begin, end, tbr)

        self._downgrader = ASCIIDowngrader()

    _prepare = lambda self, text: self._downgrader.downgrade(text)

class HiraganaTranslator(AlBhedTranslator):
    def __init__(self, begin="\"[", end="\"]", tbr="[]"):
        AlBhedTranslator.__init__(self, maps.canon["hiragana"], begin, end, tbr)

class KatakanaTranslator(AlBhedTranslator):
    def __init__(self, begin="\"[", end="\"]", tbr="[]"):
        AlBhedTranslator.__init__(self, maps.canon["katakana"], begin, end, tbr)

class CanonTranslator(AlBhedTranslator):
    def __init__(self, begin="\"[", end="\"]", tbr="[]"):
        dct = {}
        for c in maps.canon:
            dct.update(maps.canon[c])
        AlBhedTranslator.__init__(self, dct, begin, end, tbr)

        self._downgrader = ASCIIDowngrader()

    _prepare = lambda self, text: self._downgrader.downgrade(text)

class FanonTranslator(AlBhedTranslator):

    def __init__(self, begin="\"[", end="\"]", tbr="[]"):
        dct = {}
        for c in maps.canon:
            dct.update(maps.canon[c])
        for f in maps.fanon:
            dct.update(maps.fanon[f])
        AlBhedTranslator.__init__(self, dct, begin, end, tbr)
