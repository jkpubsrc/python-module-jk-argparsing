



import typing
import re
import os

from .EnumParameterType import EnumParameterType





class OptionParameter(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, displayName:str, option, ptype:EnumParameterType):
		assert isinstance(displayName, str)
		#assert isinstance(option, ArgOption)
		assert isinstance(ptype, EnumParameterType)

		self.displayName = displayName
		self.option = option

		# TODO: modularize this

		self.type = ptype
		self.strMinLength:int = None
		self.strMaxLength:int = None
		self.minValue = None
		self.maxValue = None
		self.strEnumValues = None
		self.strRegEx:str = None
		self.mustExist = None
		self.mustBeEmpty = None
		self.baseDir = None
		self.toAbsolutePath = None
		self.listMinLength:int = None
		self.listMaxLength:int = None
	#


	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __parseFile(self, sinput:str) -> str:
		assert isinstance(sinput, str)

		if self.strMinLength is not None:
			if len(sinput) < self.strMinLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.toAbsolutePath:
			if self.baseDir:
				sinput = os.path.join(self.baseDir, sinput)
			sinput = os.path.abspath(sinput)

		if self.mustExist:
			if not os.path.isfile(sinput):
				raise Exception("File specified for option " + repr(str(self.option)) + " does not exist: " + repr(sinput))			# NEW FIX

		return sinput
	#

	def __parseFileOrDirectory(self, sinput:str) -> str:
		assert isinstance(sinput, str)

		if self.strMinLength is not None:
			if len(sinput) < self.strMinLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.toAbsolutePath:
			if self.baseDir:
				sinput = os.path.join(self.baseDir, sinput)
			sinput = os.path.abspath(sinput)

		if self.mustExist:
			if not os.path.exists(sinput):
				raise Exception("File or directory specified for option " + repr(str(self.option)) + " does not exist: " + repr(sinput))

		return sinput
	#

	def __parseDirectory(self, sinput:str) -> str:
		assert isinstance(sinput, str)

		if self.strMinLength is not None:
			if len(sinput) < self.strMinLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.toAbsolutePath:
			if self.baseDir:
				sinput = os.path.join(self.baseDir, sinput)
			sinput = os.path.abspath(sinput)

		if self.mustExist:
			if not os.path.isdir(sinput):
				raise Exception("Directory specified for option " + repr(str(self.option)) + " does not exist: " + repr(sinput))

		if self.mustBeEmpty:
			if bool(os.listdir(sinput)):
				raise Exception("Directory specified for option " + repr(str(self.option)) + " is not empty: " + repr(sinput))

		return sinput
	#

	def __parseString(self, sinput:str) -> str:
		assert isinstance(sinput, str)

		if self.strEnumValues is not None:
			for v in self.strEnumValues:
				if sinput == v:
					return sinput
			raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.strMinLength is not None:
			if len(sinput) < self.strMinLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.strRegEx is not None:
			regex = re.compile(self.strRegEx)
			m = regex.match(sinput)
			if m is None:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		return sinput
	#

	def __parseStringListCommaSeparated(self, sinput:str) -> typing.List[str]:
		assert isinstance(sinput, str)

		ret:typing.List[str] = []
		for e in sinput.split(","):
			e = e.strip()
			if e:
				e = self.__parseString(e)
				ret.append(e)

		if self.listMinLength is not None:
			if len(ret) < self.listMinLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.listMaxLength is not None:
			if len(ret) > self.listMaxLength:
				raise Exception("Invalid argument value specified for option " + repr(str(self.option)) + ": " + repr(sinput))

		return ret
	#

	def __parseInt32(self, sinput:str) -> int:
		try:
			n = int(sinput)
		except:
			raise Exception("Argument is not a valid integer value at option " + repr(str(self.option)) + ": " + repr(sinput))

		if self.minValue is not None:
			if n < self.minValue:
				raise Exception("Argument too small for option " + repr(str(self.option)) + ": " + repr(sinput))
		if self.maxValue is not None:
			if n > self.maxValue:
				raise Exception("Argument too big for option " + repr(str(self.option)) + ": " + repr(sinput))
		return n
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Parse and verify the specified argument string.
	# This is the old version of the parsing method. This should be replaced by a new implementation, but right now this old version is still in use.
	#
	# @return		Returns the parsed value. This can be anything the value parser returned.
	#
	def parse(self, sinput:str) -> typing.Union[int,str,typing.List[str]]:
		assert isinstance(sinput, str)

		if self.type == EnumParameterType.String:
			return self.__parseString(sinput)
		elif self.type == EnumParameterType.Int32:
			return self.__parseInt32(sinput)
		elif self.type == EnumParameterType.File:
			return self.__parseFile(sinput)
		elif self.type == EnumParameterType.Directory:
			return self.__parseDirectory(sinput)
		elif self.type == EnumParameterType.FileOrDirectory:
			return self.__parseFileOrDirectory(sinput)
		elif self.type == EnumParameterType.ArgsList:
			raise Exception("Not supported!")
		elif self.type == EnumParameterType.StringListCommaSeparated:
			return self.__parseStringListCommaSeparated(sinput)
		else:
			raise Exception("Implementation error!")
	#

	#
	# This is the new version of the parsing method. This should replace the old version one day to avoid redundancies, but right now the old version is still in use.
	#
	# @return		object parsingResult		The value created by the parsing implementation.
	# @return		int n						The number of arguments processed. This is typically 1, except for the case that a list is expected.
	#
	def parse2(self, parameters:list, pos:int):
		assert isinstance(parameters, list)
		assert isinstance(pos, int)

		if pos == len(parameters):
			# no more data
			return None, 0

		if self.type == EnumParameterType.String:
			sinput = parameters[pos]
			return self.__parseString(sinput), 1
		elif self.type == EnumParameterType.Int32:
			sinput = parameters[pos]
			return self.__parseInt32(sinput), 1
		elif self.type == EnumParameterType.File:
			sinput = parameters[pos]
			return self.__parseFile(sinput), 1
		elif self.type == EnumParameterType.Directory:
			sinput = parameters[pos]
			return self.__parseDirectory(sinput), 1
		elif self.type == EnumParameterType.FileOrDirectory:
			sinput = parameters[pos]
			return self.__parseFileOrDirectory(sinput), 1
		elif self.type == EnumParameterType.ArgsList:
			ret = []
			n = 0
			for sinput in parameters[pos:]:
				ret.append(self.__parseString(sinput))
				n += 1
			return ret, n
		elif self.type == EnumParameterType.StringListCommaSeparated:
			raise Exception("Not yet implemented!")
		else:
			raise Exception("Implementation error!")
	#

#





















