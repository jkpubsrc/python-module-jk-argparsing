#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os

from enum import Enum




class ArgItemBase(object):

	class EnumParameterType(Enum):

		String = 1
		Int32 = 2
		File = 3
		Directory = 4
		FileOrDirectory = 5

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
			self.mustExist = None
			self.baseDir = None
			self.toAbsolutePath = None
		#



		def parse(self, sinput):
			assert isinstance(sinput, str)

			if self.type == ArgItemBase.EnumParameterType.String:
				return self.__parseString(sinput)
			elif self.type == ArgItemBase.EnumParameterType.Int32:
				return self.__parseInt32(sinput)
			elif self.type == ArgItemBase.EnumParameterType.File:
				return self.__parseFile(sinput)
			elif self.type == ArgItemBase.EnumParameterType.Directory:
				return self.__parseDirectory(sinput)
			elif self.type == ArgItemBase.EnumParameterType.FileOrDirectory:
				return self.__parseFileOrDirectory(sinput)
			else:
				raise Exception("Implementation error!")
		#



		def __parseFile(self, sinput):
			assert isinstance(sinput, str)

			if self.minLength != None:
				if len(sinput) < self.minLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.maxLength != None:
				if len(sinput) < self.maxLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.toAbsolutePath:
				if not os.path.isabs(sinput):
					if self.baseDir:
						sinput = os.path.join(self.baseDir, sinput)
					sinput = os.path.abspath(sinput)

			if self.mustExist:
				if not os.path.isfile(sinput):
					raise Exception("File specified for option " + repr(self.option) + " does not exist:: " + repr(sinput))

			return sinput
		#



		def __parseFileOrDirectory(self, sinput):
			assert isinstance(sinput, str)

			if self.minLength != None:
				if len(sinput) < self.minLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.maxLength != None:
				if len(sinput) < self.maxLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.toAbsolutePath:
				if not os.path.isabs(sinput):
					if self.baseDir:
						sinput = os.path.join(self.baseDir, sinput)
					sinput = os.path.abspath(sinput)

			if self.mustExist:
				if not os.path.exists(sinput):
					raise Exception("File or directory specified for option " + repr(str(self.option)) + " does not exist: " + repr(sinput))

			return sinput
		#



		def __parseDirectory(self, sinput):
			assert isinstance(sinput, str)

			if self.minLength != None:
				if len(sinput) < self.minLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.maxLength != None:
				if len(sinput) < self.maxLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.toAbsolutePath:
				if not os.path.exists(sinput):
					if self.baseDir:
						sinput = os.path.join(self.baseDir, sinput)
					sinput = os.path.abspath(sinput)

			if self.mustExist:
				if not os.path.isdir(sinput):
					raise Exception("Directory specified for option " + repr(str(self.option)) + " does not exist: " + repr(sinput))

			return sinput
		#



		def __parseString(self, sinput):
			assert isinstance(sinput, str)

			if self.strEnumValues != None:
				for v in self.strEnumValues:
					if sinput == v:
						return sinput
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.minLength != None:
				if len(sinput) < self.minLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.maxLength != None:
				if len(sinput) < self.maxLength:
					raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

			return sinput
		#



		def __parseInt32(self, sinput):
			try:
				n = int(sinput)
			except:
				raise Exception("Argument is not a valid integer value at option " + repr(str(self.option)) + ": " + repr(sinput))

			if self.minValue != None:
				if n < self.minValue:
					raise Exception("Argument too small for option " + repr(str(self.option)) + ": " + repr(sinput))
			if self.maxValue != None:
				if n > self.maxValue:
					raise Exception("Argument too big for option " + repr(str(self.option)) + ": " + repr(sinput))
			return n
		#

	#



	def __init__(self):
		self.__optionParameters = []
		self._isShortOption = False
	#



	@property
	def optionParameters(self):
		return self.__optionParameters
	#



	def expectFileOrDirectory(self, displayName:str, minLength:int = None, maxLength:int = None, mustExist:bool = False, toAbsolutePath:bool = False, baseDir:str = None):
		assert isinstance(displayName, str)

		if minLength is not None:
			assert isinstance(minLength, int)
		else:
			minLength = 1
		if maxLength is not None:
			assert isinstance(maxLength, int)
		if mustExist is not None:
			assert isinstance(mustExist, bool)
		if toAbsolutePath is not None:
			assert isinstance(toAbsolutePath, bool)
		if baseDir is not None:
			assert isinstance(baseDir, str)

		#if self._isShortOption:
		#	raise Exception("Short options cannot have arguments!")

		p = ArgItemBase.OptionParameter(displayName, self, ArgItemBase.EnumParameterType.FileOrDirectory)
		p.minLength = minLength
		p.maxLength = maxLength
		p.mustExist = mustExist
		p.toAbsolutePath = toAbsolutePath
		p.baseDir = baseDir
		self.__optionParameters.append(p)

		return self
	#



	def expectFile(self, displayName:str, minLength:int = None, maxLength:int = None, mustExist:bool = False, toAbsolutePath:bool = False, baseDir:str = None):
		assert isinstance(displayName, str)

		if minLength is not None:
			assert isinstance(minLength, int)
		else:
			minLength = 1
		if maxLength is not None:
			assert isinstance(maxLength, int)
		if toAbsolutePath is not None:
			assert isinstance(toAbsolutePath, bool)
		if baseDir is not None:
			assert isinstance(baseDir, str)

		#if self._isShortOption:
		#	raise Exception("Short options cannot have arguments!")

		p = ArgItemBase.OptionParameter(displayName, self, ArgItemBase.EnumParameterType.File)
		p.minLength = minLength
		p.maxLength = maxLength
		p.mustExist = mustExist
		p.toAbsolutePath = toAbsolutePath
		p.baseDir = baseDir
		self.__optionParameters.append(p)

		return self
	#



	def expectDirectory(self, displayName:str, minLength:int = None, maxLength:int = None, mustExist:bool = False, toAbsolutePath:bool = False, baseDir:str = None):
		assert isinstance(displayName, str)

		if minLength is not None:
			assert isinstance(minLength, int)
		else:
			minLength = 1
		if maxLength is not None:
			assert isinstance(maxLength, int)
		if toAbsolutePath is not None:
			assert isinstance(toAbsolutePath, bool)
		if baseDir is not None:
			assert isinstance(baseDir, str)

		#if self._isShortOption:
		#	raise Exception("Short options cannot have arguments!")

		p = ArgItemBase.OptionParameter(displayName, self, ArgItemBase.EnumParameterType.Directory)
		p.minLength = minLength
		p.maxLength = maxLength
		p.mustExist = mustExist
		p.toAbsolutePath = toAbsolutePath
		p.baseDir = baseDir
		self.__optionParameters.append(p)

		return self
	#



	def expectString(self, displayName:str, minLength:int = None, maxLength:int = None, enumValues = None):
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

		#if self._isShortOption:
		#	raise Exception("Short options cannot have arguments!")

		p = ArgItemBase.OptionParameter(displayName, self, ArgItemBase.EnumParameterType.String)
		p.minLength = minLength
		p.maxLength = maxLength
		p.strEnumValues = enumValues
		self.__optionParameters.append(p)

		return self
	#



	def expectInt32(self, displayName, minValue:int = None, maxValue:int = None):
		assert isinstance(displayName, str)

		if minValue is not None:
			assert isinstance(minValue, int)
		if maxValue is not None:
			assert isinstance(maxValue, int)

		#if self._isShortOption:
		#	raise Exception("Short options cannot have arguments!")

		p = ArgItemBase.OptionParameter(displayName, self, ArgItemBase.EnumParameterType.Int32)
		p.minValue = minValue
		p.maxValue = maxValue
		self.__optionParameters.append(p)

		return self
	#



#







