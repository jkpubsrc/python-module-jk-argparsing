﻿


from .ArgItemBase import *




class ArgCommand(ArgItemBase):

	def __init__(self, name, description):
		super().__init__()

		assert isinstance(name, str)
		assert isinstance(description, str)

		self.__name = name
		self.__description = description
	#



	@property
	def name(self):
		return self.__name
	#



	@property
	def description(self):
		return self.__description
	#



	def __str__(self):
		return self.__name
	#



#










