

import typing

from .ArgItemBase import ArgItemBase
from .ParsedArgs import ParsedArgs




ArgOption = typing.NewType("ArgOption", ArgItemBase)
#ParsedArgs = typing.NewType("ParsedArgs", object)






ON_OPTION_CALLBACK = typing.Union[typing.Callable[[ArgOption,list,ParsedArgs],None],None]

class ArgOption(ArgItemBase):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, shortName:typing.Union[str,None], longName:typing.Union[str,None], description:str):
		super().__init__()

		if shortName is not None:
			assert isinstance(shortName, str)
			assert len(shortName) == 1
		if longName is not None:
			assert isinstance(longName, str)
		assert isinstance(description, str)

		self.__shortName = shortName
		self.__longName = longName
		self.__description = description
		self.__requiredErrorMessage = None
		self.__onOption:ON_OPTION_CALLBACK = None

		self._isShortOption = self.isShortOption

		self.__providedByCommands:typing.List[str] = []
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def shortName(self) -> typing.Union[str,None]:
		return self.__shortName
	#

	@property
	def longName(self) -> typing.Union[str,None]:
		return self.__longName
	#

	@property
	def description(self) -> str:
		return self.__description
	#

	@property
	def isProvidedByCommand(self) -> bool:
		return bool(self.__providedByCommands)
	#

	#
	# Provides a list of commands that make use of this option.
	# This feature is used if commands can make use of certain options.
	# An empty list is returned if this is a general option.
	#
	@property
	def providedByCommands(self) -> typing.List[str]:
		return self.__providedByCommands
	#

	@property
	def isRequired(self) -> bool:
		return self.__requiredErrorMessage is not None
	#

	@property
	def isShortOption(self) -> bool:
		return self.__shortName is not None
	#

	@property
	def onOption(self) -> ON_OPTION_CALLBACK:
		return self.__onOption
	#

	@onOption.setter
	def onOption(self, value:ON_OPTION_CALLBACK):
		self.__onOption = value
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _invokeOpt(self, optArgs:list, parsedArgs:ParsedArgs):
		if self.__onOption is not None:
			self.__onOption(self, optArgs, parsedArgs)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		if self.__longName is not None:
			s = "--" + self.__longName
			return s

		if self.__shortName is not None:
			s = "-" + self.__shortName
			return s

		return "ArgOption(unknown)"
	#

	def __repr__(self):
		if self.__longName is not None:
			return "--" + self.__longName

		if self.__shortName is not None:
			return "-" + self.__shortName

		return "ArgOption(unknown)"
	#

	def required(self, errorMessage:str):
		assert isinstance(errorMessage, str)

		if errorMessage is None:
			raise Exception("No error message specified for required option: " + str(self))
		self.__requiredErrorMessage = errorMessage

		return self
	#

	#
	# Check if the option specified has the same short name and long name.
	#
	def hasSameNames(self, other:ArgOption) -> bool:
		assert isinstance(other, ArgOption)

		return (self.__shortName == other.__shortName) and (self.__longName == other.__longName)
	#

	#
	# Both options already have the same names.
	# Now compare both options to check if description and arguments are equal.
	#
	def ensureIsEquivalentE(self, otherOptionWithSameNames:ArgOption):
		assert isinstance(otherOptionWithSameNames, ArgOption)

		if self.__shortName != otherOptionWithSameNames.__shortName:
			raise Exception("Option objects differ in short names: {} vs. {}".format(
				repr(self.__shortName),
				repr(otherOptionWithSameNames.__shortName),
			))

		if self.__longName != otherOptionWithSameNames.__longName:
			raise Exception("Option objects differ in long names: {} vs. {}".format(
				repr(self.__longName),
				repr(otherOptionWithSameNames.__longName),
			))

		if self.__description != otherOptionWithSameNames.__description:
			raise Exception("Option objects have the same name but description differs: {} vs. {}".format(
				repr(self.__description),
				repr(otherOptionWithSameNames.__description),
			))

		if len(self._optionParameters) != len(otherOptionWithSameNames._optionParameters):
			raise Exception("Option objects {} have different number of arguments: {} vs. {}".format(
				str(self),
				len(self._optionParameters),
				len(otherOptionWithSameNames._optionParameters),
			))

		for n in range(0, len(self._optionParameters)):
			selfParam = self._optionParameters[n]
			otherParam = otherOptionWithSameNames._optionParameters[n]
			selfParam.ensureIsEquivalentE(self, otherParam)
	#

#
















