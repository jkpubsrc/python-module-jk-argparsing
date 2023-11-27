



from .ArgItemBase import *
from .ParsedArgs import ParsedArgs




ArgOption = typing.NewType("ArgOption", ArgItemBase)
#ParsedArgs = typing.NewType("ParsedArgs", object)
ON_OPTION_CALLBACK = typing.Union[typing.Callable[[ArgOption,list,ParsedArgs],None],None]

class ArgOption(ArgItemBase):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, shortName:typing.Union[str,None], longName:typing.Union[str,None], description:str, bIsProvidedByCommand:bool):
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

		self.__bIsProvidedByCommand = bIsProvidedByCommand
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
		return self.__bIsProvidedByCommand
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
			#for op in self._optionParameters:
			#	s += " " + op.displayName
			return s

		if self.__shortName is not None:
			s = "-" + self.__shortName
			#for op in self._optionParameters:
			#	s += " " + op.displayName
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
















