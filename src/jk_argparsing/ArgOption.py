



from .ArgItemBase import *




class ArgOption(ArgItemBase):



	def __init__(self, shortName, longName, description):
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
		return self.__requiredErrorMessage is not None
	#



	@property
	def isShortOption(self):
		return self.__shortName is not None
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
		if self.__onOption is not None:
			self.__onOption(self, optArgs, parsedArgs)
	#



	def __str__(self):
		if self.__longName is not None:
			s = "--" + self.__longName
			#for op in self.__optionParameters:
			#	s += " " + op.displayName
			return s

		if self.__shortName is not None:
			s = "-" + self.__shortName
			#for op in self.__optionParameters:
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



	def required(self, errorMessage):
		assert isinstance(errorMessage, str)

		if errorMessage is None:
			raise Exception("No error message specified for required option: " + str(self))
		self.__requiredErrorMessage = errorMessage

		return self
	#



#
















