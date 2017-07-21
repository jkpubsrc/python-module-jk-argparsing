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




class ArgItemBase(object):

	class EnumParameterType(Enum):
		String = 1
		Int32 = 2

	#



	class OptionParameter(object):

		def __init__(self, displayName, option, type):
			assert isinstance(displayName, str)
			#assert isinstance(option, ArgOption)
			assert isinstance(type, ArgItemBase.EnumParameterType)

			self.displayName = displayName
			self.option = option
			self.type = type
			self.minLength = None
			self.maxLength = None
			self.minValue = None
			self.maxValue = None
			self.strEnumValues = None



		def parse(self, sinput):
			assert isinstance(sinput, str)

			if self.type == ArgItemBase.EnumParameterType.String:
				return self.__parseString(sinput)
			elif self.type == ArgItemBase.EnumParameterType.Int32:
				return self.__parseInt32(sinput)
			else:
				raise Exception("Implementation error!")



		def __parseString(self, sinput):
			assert isinstance(sinput, str)

			if self.strEnumValues != None:
				for v in self.strEnumValues:
					if sinput == v:
						return sinput
				raise Exception("Invalid argument value specified for option: " + str(self.option))

			if self.minLength != None:
				if len(sinput) < self.minLength:
					raise Exception("Invalid argument value specified for option: " + str(self.option))

			if self.maxLength != None:
				if len(sinput) < self.maxLength:
					raise Exception("Invalid argument value specified for option: " + str(self.option))

			return sinput



		def __parseInt32(self, sinput):
			try:
				n = int(sinput)
			except:
				raise Exception("Argument is not a valid integer value at option: " + str(self.option))

			if self.minValue != None:
				if n < self.minValue:
					raise Exception("Argument too small for option: " + str(self.option))
			if self.maxValue != None:
				if n > self.maxValue:
					raise Exception("Argument too big for option: " + str(self.option))
			return n

	#



	def __init__(self):
		self.__optionParameters = []
		self._isShortOption = False



	@property
	def optionParameters(self):
		return self.__optionParameters



	def expectString(self, displayName, minLength = None, maxLength = None, enumValues = None):
		assert isinstance(displayName, str)

		if enumValues is not None:
			assert isinstance(enumValues, list)
			assert len(enumValues) > 0
			for v in enumValues:
				assert isinstance(v, str)

			minLength = None
			maxLength = None
		else:
			if minLength is not None:
				assert isinstance(minLength, int)
			else:
				minLength = 1
			if maxLength is not None:
				assert isinstance(maxLength, int)

		if self._isShortOption:
			raise Exception("Short options cannot have arguments!")

		p = ArgItemBase.OptionParameter(displayName, self, ArgItemBase.EnumParameterType.String)
		p.minLength = minLength
		p.maxLength = maxLength
		p.strEnumValues = enumValues
		self.__optionParameters.append(p)

		return self



	def expectInt32(self, displayName, minValue = None, maxValue = None):
		assert isinstance(displayName, str)

		if minValue is not None:
			assert isinstance(minValue, int)
		if maxValue is not None:
			assert isinstance(maxValue, int)

		if self._isShortOption:
			raise Exception("Short options cannot have arguments!")

		p = ArgItemBase.OptionParameter(displayName, self, ArgItemBase.EnumParameterType.Int32)
		p.minValue = minValue
		p.maxValue = maxValue
		self.__optionParameters.append(p)

		return self










