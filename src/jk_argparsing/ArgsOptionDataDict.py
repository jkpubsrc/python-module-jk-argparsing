#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc
import subprocess
import xml.etree.ElementTree as ElementTree

import sh







class ArgsOptionDataDict(dict):

	def set(self, key, value):
		self[key] = value







