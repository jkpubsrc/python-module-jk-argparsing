#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc
import subprocess
from enum import Enum

import sh

from .ArgItemBase import *




class ArgCommand(ArgItemBase):

	def __init__(self, name, description):
		super().__init__()

		assert isinstance(name, str)
		assert isinstance(description, str)

		self.__name = name
		self.__description = description



	@property
	def name(self):
		return self.__name



	@property
	def description(self):
		return self.__description



	def __str__(self):
		return self.__name












