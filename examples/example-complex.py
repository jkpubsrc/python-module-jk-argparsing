#!/usr/bin/env python3



import os
import time
import traceback
import sys
import abc

import sh

from jk_argparsing import *
from jk_argparsing.textmodel import *




LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse congue, orci vel interdum bibendum, nisi mauris porttitor tortor, " \
	"non tincidunt neque quam eget est. Vivamus sollicitudin urna ut elit lobortis, eget pretium est sollicitudin. Vivamus venenatis ut erat quis gravida. "\
	"Praesent vel purus finibus velit pretium eleifend."




ap = ArgsParser("myapp", "My short description")

ap.createSynopsis("myapp -x foo")
ap.createSynopsis("myapp -y bar")

ap.optionDataDefaults.set("help", False)

ap.createOption(None, "enabled", "Something is enabled.").expectString("OPT1", minLength = 2).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("my", argOptionArguments[0])
ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
ap.createOption("n", "nothing", LOREM_IPSUM)

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("apache", YEAR = 2017, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An I/O error occurred.")
ap.createReturnCode(-1, "Invalid configuration.")

ap.addDescriptionChapter("Introduction", LOREM_IPSUM)
ap.addDescriptionChapter("Usage", LOREM_IPSUM)
ap.addDescriptionChapter("Whatever", LOREM_IPSUM)

ap.addExtraChapterHead(TSection("Foo Bar Head", [
	LOREM_IPSUM,
	TSection("Foo Head", [ LOREM_IPSUM ]),
	TSection("Bar Head", [ LOREM_IPSUM ]),
]))

ap.addExtraChapterMiddle(TSection("Foo Bar Middle", [
	LOREM_IPSUM,
	TSection("Foo Middle", [ LOREM_IPSUM ]),
	TSection("Bar Middle", [ LOREM_IPSUM ]),
]))

ap.addExtraChapterEnd(TSection("Foo Bar End", [
	LOREM_IPSUM,
	TSection("Foo End", [ LOREM_IPSUM ]),
	TSection("Bar End", [ LOREM_IPSUM ]),
]))

ap.createCommand("foo", "Lorem ipsum dolor sid amet.")
ap.createCommand("bar", "The quick brown fox jumps over the lazy dog.")

parsedArgs = ap.parse()
#parsedArgs.dump()

ap.showHelp()








