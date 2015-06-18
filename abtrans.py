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
from albhed.translators import RomanCanonTranslator, FanonTranslator

class AlBhedParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument("-d", "--delimiters", nargs=2, type=str, metavar=("start", "end"),
                          help="set delimiters for proper nouns", default=("\"[", "\"]"))
        self.add_argument("-r", "--remove", type=str, metavar="rm",
                          help="characters to delete in output", default="[]")
        self.add_argument("-s", "--spiran", action="store_true",
                          help="translate to spiran")
        self.add_argument("-t", "--traditional", "--only-canon", action="store_true",
                          help="disable translation of non-canon symbols")

        self.add_argument("file", nargs=REMAINDER)

args = AlBhedParser().parse_args()

if args.traditional:
    AlBhed = RomanCanonTranslator(args.delimiters[0], args.delimiters[1], args.remove)
else:
    AlBhed = FanonTranslator(args.delimiters[0], args.delimiters[1], args.remove)

translate = AlBhed.toSpiran if args.spiran else AlBhed.toAlBhed

for line in fileinput(args.file):
    print(translate(line), end="")
