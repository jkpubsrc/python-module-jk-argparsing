


from .ArgItemBase import *
#from .ArgOption import ArgOption






ArgOption = typing.NewType("ArgOption", object)

class ArgCommand(ArgItemBase):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, argsParser, name:str, description:str, bHidden:bool = False):
		super().__init__()

		assert isinstance(name, str)
		assert isinstance(description, str)
		assert isinstance(bHidden, bool)

		self.__argsParser = argsParser
		self.__name = name
		self.__description = description
		self.__bHidden = bHidden

		self.__supportsOptions:typing.List[ArgOption] = []
	#

	################################################################################################################################
	## Public Property
	################################################################################################################################

	@property
	def name(self) -> str:
		return self.__name
	#

	@property
	def description(self) -> str:
		return self.__description
	#

	@property
	def isHidden(self) -> bool:
		return self.__bHidden
	#

	#
	# Provides a list of options that modify this command.
	#
	@property
	def supportsOptions(self) -> typing.List[ArgOption]:
		return self.__supportsOptions
	#

	################################################################################################################################
	## Helper Method
	################################################################################################################################

	################################################################################################################################
	## Public Method
	################################################################################################################################

	def __str__(self):
		return self.__name
	#

	def expectStringArgList(self,
			displayName:str,
			minLength:int = None,
			maxLength:int = None,
			strEnumValues:typing.Union[list,tuple] = None,
			strRegEx:str = None,
		):

		if self._canHaveNoMoreExpectations:
			raise Exception("After a list argument no other arguments can be used!")

		assert isinstance(displayName, str)
		if not displayName.endswith("..."):
			displayName += "..."

		if strEnumValues is not None:
			assert isinstance(strEnumValues, (tuple,list))
			assert len(strEnumValues) > 0
			for v in strEnumValues:
				assert isinstance(v, str)

			minLength = None
			maxLength = None
			strRegEx = None
		else:
			if minLength is not None:
				assert isinstance(minLength, int)
			else:
				minLength = 1
			if maxLength is not None:
				assert isinstance(maxLength, int)
			if strRegEx is not None:
				assert isinstance(strRegEx, str)
				if not strRegEx.startswith("^"):
					strRegEx = "^" + strRegEx
				if not strRegEx.endswith("$"):
					strRegEx = strRegEx + "$"

		#if self._isShortOption:
		#	raise Exception("Short options cannot have arguments!")

		p = OptionParameter(displayName, self, EnumParameterType.ArgsList)
		p.strMinLength = minLength
		p.strMaxLength = maxLength
		p.strEnumValues = strEnumValues
		p.strRegEx = strRegEx
		self._optionParameters.append(p)

		self._canHaveNoMoreExpectations = True

		return self
	#

	def registerPreparedOption(self, o:ArgOption) -> None:
		#assert isinstance(o, ArgOption)
		assert str(o.__class__.__name__) == str(ArgOption.__name__)

		self.__argsParser._registerCmdOptionCallback(self, o)
	#

	def createOption(self, shortName:typing.Union[str,None], longName:str, description:str) -> ArgOption:
		o = self.__argsParser.prepareOption(shortName, longName, description)
		self.__argsParser._registerCmdOptionCallback(self, o)
		return o
	#

#










