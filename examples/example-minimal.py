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




ap = ArgsParser("myapp", "My short description")

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")

parsedArgs = ap.parse()
#parsedArgs.dump()

ap.showHelp()








