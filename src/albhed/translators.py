######################################################################
# This program is free software. It comes without any warranty, to   #
# the extent permitted by applicable law. You can redistribute it    #
# and/or modify it under the terms of the Do What The Fuck You Want  #
# To Public License, Version 2, as published by Sam Hocevar. See     #
# http://www.wtfpl.net/ for more details.                            #
######################################################################

from . import maps
from .utils import ASCIIDowngrader

from inspect import isroutine, signature


class AlBhedTranslator(object):

    def __init__(self, al_bhed_lower, proper_noun_begin, proper_noun_end, tbr):
        self._proper_begin = proper_noun_begin
        self._proper_end   = proper_noun_end

        # copy dictionary
        al_bhed = dict(al_bhed_lower)

        # update with uppercase values
        # some characters are handled in a weird way by upper() and str.translate only
        # allows chars, not full strings
        # we therefore exclude these characters in both translation directions
        al_bhed.update({a.upper(): al_bhed[a].upper() for a in al_bhed.keys()})
        al_bhed = {a: al_bhed[a] for a in al_bhed.keys() if len(a) == 1 and len(al_bhed[a]) == 1}
        spiran = {al_bhed[key]: key for key in al_bhed.keys()}

        if(any([letter in self._proper_begin or
                letter in self._proper_end   or
                letter in tbr
                for letter in al_bhed.keys()])):
            raise ValueError("Cannot remove letters from input alphabet!")

        rm = {r: None for r in tbr}

        # build translation tables
        self._al_bhed = str.maketrans(al_bhed)
        self._spiran  = str.maketrans(spiran)
        self._remove  = str.maketrans(rm)

        # list used for storing the proper noun markers
        self._markers = []

        # lists used for pre- and postprocessing
        self._preprocessors  = []
        self._postprocessors = []

        self.addPostprocessor(lambda text: text.translate(self._remove))

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
                        ret += ntl
                        ntl = ""
                else:
                    if beg >= 0:
                        self._markers += [beg]
                    ntl += text[i]

        ret += ntl if len(self._markers) else tl.translate(dct)
        return self._postprocess(ret)

    def _prepare(self, text):
        for preprocessor in self._preprocessors:
            text = preprocessor(text)
        return text

    def _postprocess(self, text):
        for postprocessor in self._postprocessors:
            text = postprocessor(text)
        return text

    def _testprocessor(self, processor):
        assert isroutine(processor)
        sig = signature(processor)
        assert len(sig.parameters) == 1

    def addPreprocessor(self, preprocessor: "a callable, which transforms a string into a string"):
        """
        Adds a preprocessor to the translator. Preprocessors are called before the
        actual translation is done. This can be used to remove special inputs not
        handled by the translator itself or generate input.

        Keyword arguments:
            preprocessor: the preprocessor to add
        """
        self._testprocessor(preprocessor)
        self._preprocessors.append(preprocessor)

    def addPostprocessor(self, postprocessor: "a callable, which transforms a string into a string"):
        """
        Adds a postprocessor to the translator. Postprocessors are called after the
        actual translation is done. This can be used to remove markup etc.

        Keyword arguments:
            postprocessor: the preprocessor to add
        """
        self._testprocessor(postprocessor)
        self._postprocessors.append(postprocessor)

    toAlBhed = lambda self, text: self._translate(text, self._al_bhed)
    toSpiran = lambda self, text: self._translate(text, self._spiran)


class RomanCanonTranslator(AlBhedTranslator):

    def __init__(self, begin="\"[", end="\"]", tbr="[]"):
        AlBhedTranslator.__init__(self, maps.canon["roman"], begin, end, tbr)

        self._downgrader = ASCIIDowngrader()
        self.addPreprocessor(self._downgrader.downgrade)


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
        self.addPreprocessor(self._downgrader.downgrade)


class FanonTranslator(AlBhedTranslator):

    def __init__(self, begin="\"[", end="\"]", tbr="[]"):
        dct = {}
        for c in maps.canon:
            dct.update(maps.canon[c])
        for f in maps.fanon:
            dct.update(maps.fanon[f])
        AlBhedTranslator.__init__(self, dct, begin, end, tbr)
