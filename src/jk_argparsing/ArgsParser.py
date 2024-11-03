


import os
import sys
import typing

from .ArgOption import ArgOption
from .ParsedArgs import ParsedArgs
from .ArgsOptionDataDict import ArgsOptionDataDict
from .ArgUtils import ArgUtils
from .AvailableLicenseList import AvailableLicenseList
from .ArgCommand import ArgCommand
from .textmodel.VisSettings import VisSettings
from .textprimitives import *
from .textmodel import *
from .BashCompletionLocal import BashCompletionLocal
from .impl.ImplementationErrorException import ImplementationErrorException
from .impl.HelpTextData import HelpTextData
from .impl.HelpTextBuilder import HelpTextBuilder






"""
BASH_COMPLETION_DIR_CANDIDATES = [
	"~/.config/bash_completion.d/",
	"~/.bash_completion.d/",
	"~/.local/share/bash-completion/",		# compare: https://github.com/scop/bash-completion, "Q. Where should I install my own local completions?"
]
"""



class ArgsParser(object):

	################################################################################################################################
	## Nested Helper Classes
	################################################################################################################################

	"""
	class _TextTableRow2(object):

		def __init__(self, col1, col2):
			self.col1 = col1
			self.col2 = col2
		#

	#
	"""

	"""
	class _TextTableRow3(object):

		def __init__(self, col1, col2, col3):
			self.col1 = col1
			self.col2 = col2
			self.col3 = col3
		#

	#
	"""

	"""
	class _TextTable2(object):

		def __init__(self):
			self.__rows = []
		#

		def addRow(self, col1, col2):
			assert isinstance(col1, str)
			assert isinstance(col2, str)

			self.__rows.append(ArgsParser._TextTableRow2(col1, col2))
		#

		def print(self, leftMargin, columnMargin, maxWidth, outputBuffer):
			assert isinstance(leftMargin, int)
			assert isinstance(columnMargin, int)
			assert isinstance(maxWidth, int)
			assert isinstance(outputBuffer, list)

			col1size = 0
			for textTableRow in self.__rows:
				if len(textTableRow.col1) > col1size:
					col1size = len(textTableRow.col1)
			col2pos = leftMargin + col1size + columnMargin
			col2size = maxWidth - 1 - col2pos

			for textTableRow in self.__rows:
				sb = ""
				col2Wrapped = ArgUtils.wrapWords(textTableRow.col2, col2size)
				for i in range(0, leftMargin):
					sb += ' '
				sb += textTableRow.col1
				while len(sb) < col2pos:
					sb += ' '
				sb += col2Wrapped[0]
				outputBuffer.append(sb)

				if len(col2Wrapped) > 1:
					sb = ""
					while len(sb) < col2pos:
						sb += ' '

					for j in range(1, len(col2Wrapped)):
						outputBuffer.append(sb + col2Wrapped[j])
		#

	#
	"""

	"""
	class _TextTable3(object):

		def __init__(self):
			self.__rows = []
		#

		def addRow(self, col1, col2, col3):
			assert isinstance(col1, str)
			assert isinstance(col2, str)
			assert isinstance(col3, str)

			self.__rows.append(ArgsParser._TextTableRow3(col1, col2, col3))
		#

		def print(self, leftMargin, columnMargin, maxWidth, outputBuffer):
			assert isinstance(leftMargin, int)
			assert isinstance(columnMargin, int)
			assert isinstance(maxWidth, int)
			assert isinstance(outputBuffer, list)

			col1size = 0
			col2size = 0
			for textTableRow in self.__rows:
				if len(textTableRow.col1) > col1size:
					col1size = len(textTableRow.col1)
				if len(textTableRow.col2) > col2size:
					col2size = len(textTableRow.col2)
			col2pos = leftMargin + col1size + columnMargin
			col3pos = col2pos + col2size + columnMargin
			col3size = maxWidth - 1 - col3pos

			for textTableRow in self.__rows:
				sb = ""
				col3Wrapped = ArgUtils.wrapWords(textTableRow.col3, col3size)
				for i in range(0, leftMargin):
					sb += ' '
				sb += textTableRow.col1
				while len(sb) < col2pos:
					sb += ' '
				sb += textTableRow.col2
				while len(sb) < col3pos:
					sb += ' '
				sb += col3Wrapped[0]
				outputBuffer.append(sb)

				if len(col3Wrapped) > 1:
					sb = ""
					while len(sb) < col3pos:
						sb += ' '

					for j in range(1, len(col3Wrapped)):
						outputBuffer.append(sb + col3Wrapped[j])
		#

	#
	"""

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor.
	#
	# @param		str appName						This is the command the application can be executed with. This typically is the file name.
	# @param		str shortAppDescription			A short textual description what this application does.
	#
	def __init__(self, appName:str, shortAppDescription:str):
		assert isinstance(appName, str)
		assert isinstance(shortAppDescription, str)

		# defaults

		self.titleCommandsStd = "Commands"
		self.titleCommandsExtra = "Extra Commands"

		# variables

		self.__commands:typing.Dict[str,ArgCommand] = {}
		self.__commandsExtra:typing.Dict[str,ArgCommand] = {}
		self.__longArgs:typing.Dict[str,ArgOption] = {}
		self.__shortArgs:typing.Dict[str,ArgOption] = {}
		self.__options:typing.List[ArgOption] = []
		self.__optionDataDefaults = ArgsOptionDataDict()

		self.__visSettings = VisSettings()
		self.__helpTextData = HelpTextData(appName, shortAppDescription)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def visSettings(self) -> VisSettings:
		return self.__visSettings
	#

	@property
	def optionDataDefaults(self) -> ArgsOptionDataDict:
		return self.__optionDataDefaults
	#

	@property
	def appName(self) -> str:
		return self.__helpTextData.appName
	#

	@property
	def shortAppDescription(self) -> str:
		return self.__helpTextData.shortAppDescription
	#

	@property
	def allOptionNames(self) -> list:
		allOptions = []
		for o in self.__options:
			if o.shortName:
				allOptions.append("-" + o.shortName)
			if o.longName:
				allOptions.append("--" + o.longName)
		return allOptions
	#

	@property
	def allCommandNames(self) -> list:
		return list(self.__commands.keys()) + list(self.__commandsExtra.keys())
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __eatLongOption(self, optionName:str, args:list, argsPos:int, ret:ParsedArgs):
		assert isinstance(optionName, str)
		assert isinstance(args, list)
		assert isinstance(argsPos, int)
		assert isinstance(ret, ParsedArgs)

		# ----

		o = self.__longArgs.get(optionName, None)
		if o is None:
			raise Exception("No such option: " + optionName)

		if argsPos + len(o.optionParameters) > len(args):
			raise Exception("Option " + o.longName + " expects " + str(len(o.optionParameters)) + " arguments!")

		optionArgs = []
		for i in range(0, len(o.optionParameters)):
			optionArgs.append(o.optionParameters[i].parse(args[argsPos + i]))
		argsPos += len(o.optionParameters)

		o._invokeOpt(optionArgs, ret)

		return (o, argsPos)
	#

	def __eatShortOption(self, optionName:str, args:list, argsPos:int, ret:ParsedArgs):
		assert isinstance(optionName, str)
		assert isinstance(args, list)
		assert isinstance(argsPos, int)
		assert isinstance(ret, ParsedArgs)

		# ----

		o = self.__shortArgs.get(optionName, None)
		if o is None:
			raise Exception("No such option: " + optionName)

		if argsPos + len(o.optionParameters) > len(args):
			raise Exception("Option " + o.longName + " expects " + str(len(o.optionParameters)) + " arguments!")

		optionArgs = []
		for i in range(0, len(o.optionParameters)):
			optionArgs.append(o.optionParameters[i].parse(args[argsPos + i]))
		argsPos += len(o.optionParameters)

		o._invokeOpt(optionArgs, ret)

		return (o, argsPos)
	#

	"""
	def __eatShortOption(self, optionName, ret):
		assert isinstance(optionName, str)
		assert isinstance(ret, ParsedArgs)

		o = self.__shortArgs.get(optionName, None)
		if o is None:
			raise Exception("No such option: " + optionName)

		o._invokeOpt(None, ret)

		return o
	#
	"""

	def _registerCmdOptionCallback(self, cmd:ArgCommand, option:ArgOption):
		assert isinstance(cmd, ArgCommand)
		assert isinstance(option, ArgOption)

		bSkip = False
		cand1 = None
		if option.shortName is not None:
			cand1 = self.__shortArgs.get(option.shortName)
			if cand1:
				option.ensureIsEquivalentE(cand1)
				option = cand1
				bSkip = True

		if option.longName is not None:
			cand2 = self.__longArgs.get(option.longName)
			if cand2:
				option.ensureIsEquivalentE(cand2)
				option = cand2
				bSkip = True

		if (cand1 is not None) and (cand2 is not None) and (cand1 != cand2):
			raise Exception("For --{} already another option is registered: {}".format(option.longName, str(cand2)))

		cmd.supportsOptions.append(option)
		option.providedByCommands.append(cmd.name)

		if not bSkip:
			self.registerPreparedOption(option)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def getCommand(self, name:str) -> typing.Union[ArgCommand,None]:
		assert isinstance(name, str)

		# ----

		ret = self.__commands.get(name)
		if ret:
			return ret

		ret = self.__commandsExtra.get(name)
		if ret:
			return ret

		return None
	#

	def hasCommand(self, name:str) -> bool:
		assert isinstance(name, str)

		# ----

		return (name in self.__commands) or (name in self.__commandsExtra)
	#

	def createCommand(self, name:str, description:str, bHidden:bool = False) -> ArgCommand:
		cmd = self.prepareCommand(name, description, bHidden)
		self.registerPreparedCommand(cmd)
		return cmd
	#

	def prepareCommand(self, name:str, description:str, bHidden:bool = False) -> ArgCommand:
		assert isinstance(name, str)
		assert name
		assert isinstance(description, str)
		assert description
		assert isinstance(bHidden, bool)

		# ----

		o = ArgCommand(self, name, description, bHidden)
		return o
	#

	def registerPreparedCommand(self, cmd:ArgCommand) -> None:
		assert isinstance(cmd, ArgCommand)

		# ----

		if (cmd.name in self.__commands) or (cmd.name in self.__commandsExtra):
			raise Exception("A command named '" + cmd.name + "' already exists!")
		self.__commands[cmd.name] = cmd
	#

	def createExtraCommand(self, name:str, description:str) -> ArgCommand:
		assert isinstance(name, str)
		assert name
		assert isinstance(description, str)
		assert description

		# ----

		o = ArgCommand(name, description)
		if (o.name in self.__commands) or (o.name in self.__commandsExtra):
			raise Exception("A command named '" + o.name + "' already exists!")
		self.__commandsExtra[o.name] = o

		return o
	#

	################################################################################################################################

	def getOption(self, name:str) -> typing.Union[ArgOption,None]:
		assert isinstance(name, str)

		# ----

		for opt in self.__options:
			if name == opt.shortName:
				return opt
			if name == opt.longName:
				return opt

		return None
	#

	def hasOption(self, name:str) -> bool:
		assert isinstance(name, str)

		# ----

		for opt in self.__options:
			if name == opt.shortName:
				return True
			if name == opt.longName:
				return True

		return False
	#

	def createOption(self, shortName:typing.Union[str,None], longName:str, description:str) -> ArgOption:
		o = self.prepareOption(shortName, longName, description)
		self.registerPreparedOption(o)
		return o
	#

	def prepareOption(self, shortName:typing.Union[str,None], longName:str, description:str) -> ArgOption:
		if shortName is not None:
			assert isinstance(shortName, str)
			assert len(shortName) == 1

		if longName is not None:
			assert isinstance(longName, str)
			assert longName

		assert isinstance(description, str)
		assert description

		if (shortName is None) and (longName is None):
			raise Exception("Arguments need at least a long or a short name!")

		# ----

		return ArgOption(shortName, longName, description)
	#

	def registerPreparedOption(self, o:ArgOption) -> None:
		assert isinstance(o, ArgOption)

		# ----

		if o.shortName is not None:
			if o.shortName in self.__shortArgs:
				raise Exception("Duplicate short argument: '-" + o.shortName + "'")
			self.__shortArgs[o.shortName] = o

		if o.longName is not None:
			if o.longName in self.__longArgs:
				raise Exception("Duplicate long argument: '--" + o.longName + "'")
			self.__longArgs[o.longName] = o

		self.__options.append(o)
	#

	# def createCommandOption(self, cmd:typing.Union[ArgCommand,str,None], shortName:typing.Union[str,None], longName:str, description:str = None) -> ArgOption:
	# 	if cmd is not None:
	# 		assert isinstance(cmd, (ArgCommand,str))
	# 		if isinstance(cmd, ArgCommand):
	# 			cmd = cmd.name
	# 		assert cmd

	# 	if shortName is not None:
	# 		assert isinstance(shortName, str)
	# 		assert len(shortName) == 1

	# 	if longName is not None:
	# 		assert isinstance(longName, str)
	# 		assert longName

	# 	if (shortName is None) and (longName is None):
	# 		raise Exception("Arguments need at least a long or a short name!")

	# 	if description is not None:
	# 		assert isinstance(description, str)
	# 		assert description

	# 	# ----

	# 	# find a possibly existing option object

	# 	oShort = self.__shortArgs.get(shortName) if shortName is not None else None
	# 	oLong = self.__longArgs.get(longName) if longName is not None else None

	# 	if oShort is None:
	# 		if oLong is None:
	# 			# oShort == None, oLong == None

	# 			if description is None:
	# 				raise Exception("Arguments that have not been predefined need to have a description!")
				
	# 			# create new and register it
	# 			o = ArgOption(shortName, longName, description)
	# 			if shortName is not None:
	# 				self.__shortArgs[o.shortName] = o
	# 			if longName is not None:
	# 				self.__shortArgs[o.longName] = o
	# 			self.__options.append(o)

	# 		else:
	# 			# oShort == None, oLong != None

	# 			if not oLong.isProvidedByCommand:
	# 				raise Exception("A global option is already defined matching '--" + longName + "'")
	# 			o = oLong

	# 	else:
	# 		if oLong is None:
	# 			# oShort != None, oLong == None

	# 			if not oShort.isProvidedByCommand:
	# 				raise Exception("A global option is already defined matching '-" + shortName + "'")
	# 			o = oShort
	# 		else:
	# 			# oShort != None, oLong != None

	# 			# we can't arrive here
	# 			raise ImplementationErrorException()

	# 	# ----

	# 	if cmd:
	# 		o.providedByCommands.append(cmd)

	# 	return o
	# #

	#
	# Check if the specified short option already exists
	#
	def hasShortOption(self, shortName:str) -> bool:
		assert isinstance(shortName, str)
		assert len(shortName) == 1

		# ----

		for ao in self.__options:
			if ao.shortName == shortName:
				return True

		return False
	#

	#
	# Check if the specified long option already exists
	#
	def hasLongOption(self, longName:str) -> bool:
		assert isinstance(longName, str)
		assert len(longName) == 1

		# ----

		for ao in self.__options:
			if ao.longName == longName:
				return True

		return False
	#

	################################################################################################################################

	#
	# Add information about an author of this software.
	#
	def createAuthor(self, name:str, email:str = None, description:str = None):
		assert isinstance(name, str)
		assert name
		if email is not None:
			assert isinstance(email, str)
			assert email

		self.__helpTextData.authorsList.append((name, email, description))

		return self
	#

	#
	# Create synopsis information
	#
	def createSynopsis(self, synopsis:str):
		assert isinstance(synopsis, str)
		assert synopsis

		self.__helpTextData.synopsisList.append(synopsis)

		return self
	#

	#
	# Add a return code.
	# If you add the exact same return code and description again this registration is ignored.
	#
	# @param		int returnCode		The return code (= program exit status code)
	# @param		str description		The description for this return code
	#
	def createReturnCode(self, returnCode:int, description:str):
		assert isinstance(returnCode, int)
		assert isinstance(description, str)

		for _existingRC, _existingDescr in self.__helpTextData.returnCodesList:
			if (_existingRC == returnCode) and (_existingDescr == description):
				return self

		self.__helpTextData.returnCodesList.append((returnCode, description))

		return self
	#

	def setLicense(self, licenseID:str, **kwargs):
		assert isinstance(licenseID, str)

		availableLicenseList = AvailableLicenseList()
		self.__helpTextData.licenseTextLines = availableLicenseList.getText(licenseID, **kwargs)
		if self.__helpTextData.licenseTextLines is None:
			raise Exception("No such license: " + licenseID)

		return self
	#

	def addDescriptionChapter(self, chapterName:typing.Union[str,None], paragraphs:typing.Sequence = None) -> TSection:
		if chapterName is None:
			for p in paragraphs:
				self.__helpTextData.descriptionChapters.append(TBlock(p))
			sec = None

		else:
			assert isinstance(chapterName, str)
			if isinstance(paragraphs, str):
				sec = TSection(chapterName, [ paragraphs ])
			else:
				sec = TSection(chapterName, paragraphs)
			self.__helpTextData.descriptionChapters.append(sec)

		return sec
	#

	def addExtraChapterHead(self, section:TSection):
		assert isinstance(section, TSection)
		self.__helpTextData.extraHeadChapters.append(section)
		return self
	#

	def addExtraChapterMiddle(self, section:TSection):
		assert isinstance(section, TSection)
		self.__helpTextData.extraMiddleChapters.append(section)
		return self
	#

	def addExtraChapterEnd(self, section:TSection):
		assert isinstance(section, TSection)
		self.__helpTextData.extraEndChapters.append(section)
		return self
	#

	################################################################################################################################

	def showHelp(self, bColor:bool = None):
		print()
		for line in self.buildHelpText(bColor = bColor):
			print(line)
		print()
	#

	def buildHelpText(self, bColor:bool = None) -> typing.List[str]:
		helpTextBuilder = HelpTextBuilder(
			self.__options,
			self.__commands,
			self.__commandsExtra,
			self.__visSettings,
			self.__helpTextData,
		)

		return helpTextBuilder.buildHelpText(bColor)
	#

	#
	# Parse the specified arguments or the program arguments.
	#
	# @param	str[] args			(optional) If specified the specified arguments are parsed.
	#								If <c>None</c> is specified (= the default) the program arguments are retrieved via <c>sys.argv</c> and parsed.
	#
	def parse(self, args:typing.Iterable[str] = None) -> ParsedArgs:
		if args is None:
			args = list(sys.argv)
			args = args[1:]
		else:
			assert isinstance(args, list)
			for a in args:
				assert isinstance(a, str)

		# ----

		ret = ParsedArgs(self.__commands)
		for key in self.__optionDataDefaults:
			ret.optionData[key] = self.__optionDataDefaults[key]

		optionsRequired:typing.List[ArgOption] = []
		for ao in self.__options:
			if ao.isRequired:
				optionsRequired.append(ao)

		# check options
		argsPos = 0
		while argsPos < len(args):
			#print("next: " + str(argsPos) + ", " + args[argsPos])
			current = args[argsPos]
			argsPos += 1

			if len(current) >= 2:
				if current[0] == '-':
					if current[1] == '-':
						# long option
						#print("current argsPos: " + str(argsPos))
						(op, argsPos) = self.__eatLongOption(current[2:], args, argsPos, ret)
						#print("new argsPos: " + str(argsPos))
						if op in optionsRequired:
							optionsRequired.remove(op)
						if ret.terminate:
							break
					else:
						# short option
						for i in range(1, len(current)):
							(op, argsPos) = self.__eatShortOption(current[i], args, argsPos, ret)
							if op in optionsRequired:
								optionsRequired.remove(op)
							if ret.terminate:
								break
					continue

			argsPos -= 1
			break

		if ret.terminate:
			return None

		if len(optionsRequired) > 0:
			raise Exception("Option required: " + str(optionsRequired[0]))

		ret.programArgs = args[argsPos:]

		return ret
	#

	"""
	#
	# @param	bool bWithLocal		If <c>True</c> a complete command is added for running the current script from "./" as well.
	#								This is not needed for system wide installations.
	#
	def createBashCompletionFileText(self, bWithLocal:bool = False):
		allOptions = []
		for o in self.__options:
			if o.shortName:
				allOptions.append("-" + o.shortName)
			if o.longName:
				allOptions.append("--" + o.longName)

		allCommands = list(self.__commands.keys()) + list(self.__commandsExtra.keys())

		lines = [
			"_" + self.__appName + "_()",
			"{",
			"	local cur prev opts",
			"	COMPREPLY=()",
			"	cur=\"${COMP_WORDS[COMP_CWORD]}\"",
			"	prev=\"${COMP_WORDS[COMP_CWORD-1]}\"",
			"	opts=\"" + " ".join(allOptions) + "\"",
			"	cmds=\"" + " ".join(allCommands) + "\"",
			"",
			"	if [[ ${cur} == -* ]] ; then",
			"		COMPREPLY=( $(compgen -W \"${opts}\" -- ${cur}) )",
			"		return 0",
			"	else",
			"		COMPREPLY=( $(compgen -W \"${cmds}\" -- ${cur}) )",
			"		return 0",
			"	fi",
			"}",
			"complete -F _" + self.__appName + "_ " + self.__appName,
		]
		if bWithLocal:
			lines.append("complete -F _" + self.__appName + "_ ./" + self.__appName)
		lines.append("")

		return "\n".join(lines)
	#

	#
	# This method generates the local bash completion file path. Or throws an exception if this feature is not configured or not supported.
	#
	def generateLocalBashCompletionFilePath(self, dirCandidates:list=None) -> str:
		if os.name == 'nt':
			raise Exception("Sorry, the bash completion feature is only supported for non-Windows operating systems.")

		# ----

		if dirCandidates is None:
			dirCandidates = BASH_COMPLETION_DIR_CANDIDATES
		else:
			for dc in dirCandidates:
				assert isinstance(dc, str)

		# ----

		homeDir = pwd.getpwuid(os.getuid()).pw_dir
		assert isinstance(homeDir, str)
		assert os.path.isdir(homeDir)

		installDirPath = None
		for dc in dirCandidates:
			if dc.startswith("~/"):
				p = os.path.join(homeDir, dc[2:])
				if os.path.isdir(p):
					installDirPath = p
					break

		if not installDirPath:
			raise Exception("No installation path exists! (You might want to create: '{}')".format(BASH_COMPLETION_DIR_CANDIDATES[0]))

		# ----

		return os.path.join(installDirPath, self.__appName.replace(".", "_"))
	#

	def installLocalBashCompletionFile(self, dirCandidates:list=None, printFunc=None, bQuiet:bool = True, bRaiseExceptionIfNoCompletionDirExists:bool = False) -> bool:
		if printFunc is not None:
			assert callable(printFunc)
		else:
			printFunc = print

		# ----

		if bRaiseExceptionIfNoCompletionDirExists:
			# allow raising exceptions
			installFilePath = generateLocalBashCompletionFilePath(dirCandidates)
		else:
			# no exceptions allowed
			try:
				installFilePath = generateLocalBashCompletionFilePath(dirCandidates)
			except Exception as ee:
				if not bQuiet:
					printFunc(str(ee))
				return False

		# ----

		existingCompletionFileText = None
		if os.path.isfile(installFilePath):
			with open(installFilePath, "r") as f:
				existingCompletionFileText = f.read()

		newCompletionFileText = self.createBashCompletionFileText(bWithLocal=True)
		if existingCompletionFileText != newCompletionFileText:
			if not bQuiet:
				printFunc("Now installing bash completion file: {}".format(installFilePath))

			with open(installFilePath, "w") as f:
				f.write(newCompletionFileText)

		# ----

		return True
	#
	"""

	def installLocalBashCompletion(self, absAppFilePath:str, bDebug:bool = False):
		bc = BashCompletionLocal(bDebug=bDebug)
		bc._writeDebugData("absAppFilePath =", absAppFilePath)
		bc.install(absAppFilePath, self.allOptionNames, self.allCommandNames, bQuiet=True)
	#

#




