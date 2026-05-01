


import typing

from ..textmodel import *







class AuthorTuple(typing.NamedTuple):
	name:str
	email:str
	description:str
#



class ReturnCodeTuple(typing.NamedTuple):
	code:str
	description:str
#



class EnvVarTuple(typing.NamedTuple):
	varName:str
	description:str
#



#
# Holds most of the data required to build the help text
#
class HelpTextData(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, appName:str, shortAppDescription:str):

		# defaults

		self.titleCommandsStd:str = "Commands"
		self.titleCommandsExtra:str = "Extra Commands"
		self.titleCommandsHidden:str = "Hidden Commands"

		# variables

		self.appName:str = appName
		self.shortAppDescription:str = shortAppDescription

		self.synopsisList:list[str] = []										# stores strings that hold the synopsis
		self.authorsList:list[AuthorTuple|tuple[str,str,str]] = []	# stores tuples of `(author-name, author-email, author-description)`
		self.returnCodesList:list[ReturnCodeTuple|tuple[int,str]] = []				# stores tuples of `(return-code, description)`
		self.envVarsList:list[EnvVarTuple|tuple[str,str]] = []				# stores tuples of `(return-code, description)`
		self.licenseTextLines:list[str]|None = None

		self.descriptionChapters:list[TBlock|TSection] = []
		self.extraHeadChapters:list[TSection] = []
		self.extraMiddleChapters:list[TSection] = []
		self.extraEndChapters:list[TSection] = []
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#






