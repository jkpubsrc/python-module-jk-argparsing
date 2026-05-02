

import typing

import jk_typing
import jk_utils
import jk_logging
import jk_json
import jk_prettyprintobj

from .AuthorTuple import AuthorTuple
from .ReturnCodeTuple import ReturnCodeTuple
from .EnvVarTuple import EnvVarTuple
from .VisSettings import VisSettings
from ..ArgOption import ArgOption
from ..ArgCommand import ArgCommand
from ..textmodel.TBlock import TBlock
from ..textmodel.TList import TList
from ..textmodel.TSection import TSection





#
# Holds all the data required to build the help text.
#
class HelpTextSrcData(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			appName:str,
			shortAppDescription:str,
			options:list[ArgOption],
			noCommand:ArgCommand|None,
			commands:dict[str,ArgCommand],
			commandsExtra:dict[str,ArgCommand],
			visSettings:VisSettings,
		):

		# defaults; mey be modified

		self.titleCommandsStd:str = "Commands"
		self.titleCommandsExtra:str = "Extra Commands"
		self.titleCommandsHidden:str = "Hidden Commands"

		# data structures

		self.options = options
		self.noCommand = noCommand
		self.commands = commands
		self.commandsExtra = commandsExtra
		self.visSettings = visSettings

		# regular variables

		self.appName:str = appName
		self.shortAppDescription:str = shortAppDescription

		self.synopsisList:list[str] = []
		self.authorsList:list[AuthorTuple] = []
		self.returnCodesList:list[ReturnCodeTuple] = []
		self.envVarsList:list[EnvVarTuple] = []
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

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#




