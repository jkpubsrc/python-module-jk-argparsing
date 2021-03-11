#!/usr/bin/env python3
# -*- coding: utf-8 -*-



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

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")

parsedArgs = ap.parse()
#parsedArgs.dump()

ap.showHelp()








