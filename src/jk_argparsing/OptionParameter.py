



import typing
import re
import os

from .EnumParameterType import EnumParameterType







OptionParameter = typing.NewType("OptionParameter", object)

class OptionParameter(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, displayName:str, commandOrOption, ptype:EnumParameterType):
		assert isinstance(displayName, str)
		#assert isinstance(option, ArgOption)
		assert isinstance(ptype, EnumParameterType)

		self.displayName = displayName

		self.commandOrOption = commandOrOption
		self.__bIsOption = commandOrOption.__class__.__name__ == "ArgOption"
		self.__bIsCommand = commandOrOption.__class__.__name__ == "ArgCommand"

		if not (self.__bIsOption ^ self.__bIsCommand):
			raise Exception("Implementation error!")

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
		self.intEnumValues = None

		self.__kindStr = "command" if self.__bIsCommand else "option"
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
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.toAbsolutePath:
			if self.baseDir:
				sinput = os.path.join(self.baseDir, sinput)
			sinput = os.path.abspath(sinput)

		if self.mustExist:
			if not os.path.isfile(sinput):
				raise Exception("File specified for {} {} does not exist: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		return sinput
	#

	def __parseFileOrDirectory(self, sinput:str) -> str:
		assert isinstance(sinput, str)

		if self.strMinLength is not None:
			if len(sinput) < self.strMinLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.toAbsolutePath:
			if self.baseDir:
				sinput = os.path.join(self.baseDir, sinput)
			sinput = os.path.abspath(sinput)

		if self.mustExist:
			if not os.path.exists(sinput):
				raise Exception("File or directory specified for {} {} does not exist: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		return sinput
	#

	def __parseDirectory(self, sinput:str) -> str:
		assert isinstance(sinput, str)

		if self.strMinLength is not None:
			if len(sinput) < self.strMinLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.toAbsolutePath:
			if self.baseDir:
				sinput = os.path.join(self.baseDir, sinput)
			sinput = os.path.abspath(sinput)

		if self.mustExist:
			if not os.path.isdir(sinput):
				raise Exception("Directory specified for {} {} does not exist: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.mustBeEmpty:
			if bool(os.listdir(sinput)):
				raise Exception("Directory specified for {} {} is empty: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		return sinput
	#

	def __parseString(self, sinput:str) -> str:
		assert isinstance(sinput, str)

		if self.strEnumValues is not None:
			for v in self.strEnumValues:
				if sinput == v:
					return sinput
			raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.strMinLength is not None:
			if len(sinput) < self.strMinLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.strMaxLength is not None:
			if len(sinput) < self.strMaxLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.strRegEx is not None:
			regex = re.compile(self.strRegEx)
			m = regex.match(sinput)
			if m is None:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

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
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.listMaxLength is not None:
			if len(ret) > self.listMaxLength:
				raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		return ret
	#

	def __parseInt32(self, sinput:str) -> int:
		try:
			n = int(sinput)
		except:
			raise Exception("Argument is not a valid integer value at {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.intEnumValues is not None:
			for v in self.intEnumValues:
				if sinput == v:
					return n
			raise Exception("Invalid argument value specified for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		if self.minValue is not None:
			if n < self.minValue:
				raise Exception("Argument too small for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))
		if self.maxValue is not None:
			if n > self.maxValue:
				raise Exception("Argument too big for {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))

		return n
	#

	def __parseBoolean(self, sinput:str) -> bool:
		sinput = sinput.lower()

		if sinput in ("on", "yes", "true"):
			return True
		if sinput in ("off", "no", "false"):
			return False

		try:
			n = int(sinput)
			if n == 0:
				return False
			if n == 1:
				return True
		except:
			pass

		raise Exception("Argument is not a valid boolean value at {} {}: {}".format(self.__kindStr, repr(str(self.commandOrOption)), repr(sinput)))
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
		elif self.type == EnumParameterType.Bool:
			return self.__parseBoolean(sinput)
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
			sinput = parameters[pos]
			return self.__parseStringListCommaSeparated(sinput), 1
		elif self.type == EnumParameterType.Bool:
			sinput = parameters[pos]
			return self.__parseBoolean(sinput), 1
		else:
			raise Exception("Implementation error!")
	#

	#
	# Both options already seem to be equivalent. Now let's check the options parameters if they are equivalent.
	#
	# NOTE: Only the option name and type are checked. Constraints are ignored.
	#
	def ensureIsEquivalentE(self, option, otherParam:OptionParameter):
		assert isinstance(otherParam, OptionParameter)

		if self.displayName != otherParam.displayName:
			raise Exception("Option objects {} have different parameters: {} vs. {}".format(
				repr(option),
				str(self),
				str(otherParam),
			))

		if self.type != otherParam.type:
			raise Exception("Option objects {} have different parameter types: {} vs. {}".format(
				repr(option),
				str(self),
				str(otherParam),
			))
	#
	
	def __str__(self):
		return "<{}:{}>".format(self.displayName, self.type)
	#

#





















