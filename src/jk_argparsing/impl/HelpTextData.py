


import os
import sys
import typing

from ..textmodel import *




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

		self.titleCommandsStd = "Commands"
		self.titleCommandsExtra = "Extra Commands"

		# variables

		self.appName = appName
		self.shortAppDescription:str = shortAppDescription

		self.synopsisList:typing.List[str] = []								# stores strings that hold the synopsis
		self.authorsList:typing.List[typing.Tuple[str,str,str]] = []		# stores tuples of `(author-name, author-email, author-description)`
		self.returnCodesList:typing.List[typing.Tuple[int,str]] = []		# stores tuples of `(return-code, description)`
		self.licenseTextLines:typing.Union[typing.List[str],None] = None

		self.descriptionChapters:typing.List[TBlock,TSection] = []
		self.extraHeadChapters:typing.List[TSection] = []
		self.extraMiddleChapters:typing.List[TSection] = []
		self.extraEndChapters:typing.List[TSection] = []
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






