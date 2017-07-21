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




class ArgOption(ArgItemBase):



	def __init__(self, shortName, longName, description):
		super().__init__()

		if shortName != None:
			assert isinstance(shortName, str)
			assert len(shortName) == 1
		if longName != None:
			assert isinstance(longName, str)
		assert isinstance(description, str)

		self.__shortName = shortName
		self.__longName = longName
		self.__description = description
		self.__requiredErrorMessage = None
		self.__onOption = None

		self._isShortOption = self.isShortOption
	#



	@property
	def shortName(self):
		return self.__shortName
	#



	@property
	def longName(self):
		return self.__longName
	#



	@property
	def description(self):
		return self.__description
	#



	@property
	def isRequired(self):
		return self.__requiredErrorMessage != None
	#



	@property
	def isShortOption(self):
		return self.__shortName != None
	#



	@property
	def onOption(self):
		return self.__onOption
	#



	@onOption.setter
	def onOption(self, value):
		self.__onOption = value
	#



	def _invokeOpt(self, optArgs, parsedArgs):
		if self.__onOption != None:
			self.__onOption(self, optArgs, parsedArgs)
	#



	def __str__(self):
		if self.__longName != None:
			return "--" + self.__longName
		if self.__shortName != None:
			s = "--" + self.__longName
			for op in self.__optionParameters:
				s += " " + op.displayName
		return "ArgOption(unknown)"
	#



	def required(self, errorMessage):
		assert isinstance(errorMessage, str)

		if errorMessage is None:
			raise Exception("No error message specified for required option: " + str(self))
		self.__requiredErrorMessage = errorMessage

		return self
	#


















