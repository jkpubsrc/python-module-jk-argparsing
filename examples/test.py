#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc

import sh

from jk_argparsing import *





ap = ArgsParser("myapp", "My short description")

ap.optionDataDefaults.set("help", False)

ap.createOption(None, 'enabled', "Something is enabled.").expectString("OPT1", minLength = 2).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("my", argOptionArguments[0])
ap.createOption('h', 'help', "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
ap.createOption('n', 'nothing', "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse congue, orci vel interdum bibendum, nisi mauris porttitor tortor, non tincidunt neque quam eget est. Vivamus sollicitudin urna ut elit lobortis, eget pretium est sollicitudin. Vivamus venenatis ut erat quis gravida. Praesent vel purus finibus velit pretium eleifend.")

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("mit", YEAR = 2017, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An I/O error occurred.")
ap.createReturnCode(-1, "Invalid configuration.")

parsedArgs = ap.parse()
#parsedArgs.dump()

ap.showHelp()








