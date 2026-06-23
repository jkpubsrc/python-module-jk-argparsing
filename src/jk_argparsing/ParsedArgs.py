


import typing



from .ArgsOptionDataDict import ArgsOptionDataDict
from .ArgCommand import ArgCommand
from .NoSuchCommandException import NoSuchCommandException





class NextCommand(typing.NamedTuple):
	cmdName:str|None
	parsedArgs:list[None|int|bool|str|list[str]]|None

	def __str__(self):
		return f"NextCommand<( cmdName={self.cmdName!r}, parsedArgs={self.parsedArgs} )>"
	#

	def __repr__(self):
		return f"NextCommand<( cmdName={self.cmdName!r}, parsedArgs={self.parsedArgs} )>"
	#

#






#
# This class contains the results of command line parsing.
#
class ParsedArgs(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, noCommand:ArgCommand|None, allCommands:typing.Dict[str,ArgCommand]):
		self.__noCommand:ArgCommand|None = noCommand
		self.__allCommands = allCommands
		self.__optionData = ArgsOptionDataDict()
		self.terminate = False
		self.programArgs = []
		self.__argsPos = 0
		self.__bError = False					# NEW IMPL
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# This dictionary is ready to store all data parsed from processing command
	# line options.
	#
	@property
	def optionData(self) -> ArgsOptionDataDict:
		return self.__optionData
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def dump(self, prefix:str = None, printFunction = None):
		if prefix is None:
			prefix = ""
		else:
			assert isinstance(prefix, str)

		if printFunction is None:
			printFunction = print
		else:
			assert callable(printFunction)

		printFunction(prefix + "ParsedArgs[")
		printFunction(prefix + "\toptionData: " + str(self.__optionData))
		printFunction(prefix + "\tterminate: " + str(self.terminate))
		printFunction(prefix + "\tprogramArgs: " + str(self.programArgs))
		printFunction(prefix + "]")
	#

	"""
	def parseNextCommand(self) -> tuple:
		if self.__bError:															# NEW IMPL
			raise Exception("There have been previous parsing errors!")				# NEW IMPL

		if self.__argsPos >= len(self.programArgs):
			return (None, None)

		nextCmdCandidate = self.programArgs[self.__argsPos]
		cmd = self.__commands.get(nextCmdCandidate, None)
		if cmd is None:
			self.__bError = True													# NEW IMPL
			raise Exception("Unknown command: \"" + nextCmdCandidate + "\"")
		self.__argsPos += 1

		if self.__argsPos + len(cmd.optionParameters) > len(self.programArgs):
			self.__bError = True													# NEW IMPL
			raise Exception("Option " + cmd.name + " expects " + str(len(cmd.optionParameters)) + " arguments!")

		optionArgs = []
		for i in range(0, len(cmd.optionParameters)):
			optionArgs.append(cmd.optionParameters[i].parse(self.programArgs[self.__argsPos + i]))
		self.__argsPos += len(cmd.optionParameters)

		return (cmd.name, optionArgs)
	#
	"""

	#
	# Parse the program arguments from the command line (if the parser is configured for not parsing commands).
	#
	def parseNoCommand(self) -> list[None|int|bool|str|list[str]]:
		if self.__bError:															# NEW IMPL
			raise Exception("There have been previous parsing errors!")				# NEW IMPL

		if self.__noCommand is None:
			raise Exception("Use parseNextCommand() because this parser is configured for commands!")

		if self.__argsPos >= len(self.programArgs):
			# end of parsing has been reached
			return None

		# now process the arguments of the command

		parsedArgs:list[None|int|bool|str|list[str]] = []
		for cmdOptionParam in self.__noCommand.optionParameters:
			_parsingResult, _n = cmdOptionParam.parse2(self.programArgs, self.__argsPos)
			if _n <= 0:
				raise Exception("More arguments required!")
			parsedArgs.append(_parsingResult)
			self.__argsPos += _n

		# return data

		return parsedArgs
	#

	#
	# Parse the next command in the command line (if the parser is configured for parsing commands).
	#
	# Note: <c>self.__argsPos</c> stores the current parsing cursor.
	#
	# @return		str cmdName									The name of the command. <c>None</c> is returned if there is no more data to process.
	# @return		list<null|int|bool|str|str[]> parsedArgs	The arguments for this command. <c>None</c> is returned if there is no more data to process.
	#
	def parseNextCommand(self) -> NextCommand:
		if self.__bError:															# NEW IMPL
			raise Exception("There have been previous parsing errors!")				# NEW IMPL

		if self.__noCommand is not None:
			raise Exception("Use parseNoCommand() because this parser is configured for commands!")

		if self.__argsPos >= len(self.programArgs):
			# end of parsing has been reached
			return NextCommand(None, None)

		# retrieve the command in the line

		nextCmdCandidate = self.programArgs[self.__argsPos]
		cmd = self.__allCommands.get(nextCmdCandidate, None)
		if cmd is None:
			self.__bError = True													# NEW IMPL
			raise NoSuchCommandException(nextCmdCandidate, sorted(self.__allCommands.keys()))
		self.__argsPos += 1

		# now process the arguments of the command

		parsedArgs:list[None|int|bool|str|list[str]] = []
		for cmdOptionParam in cmd.optionParameters:
			_parsingResult, _n = cmdOptionParam.parse2(self.programArgs, self.__argsPos)
			if _n <= 0:
				raise Exception("Option " + cmd.name + " expects more arguments!")
			parsedArgs.append(_parsingResult)
			self.__argsPos += _n

		# return data

		return NextCommand(cmd.name, parsedArgs)
	#

	"""
	def parseCommands(self):														# NEW IMPL
		if self.__bError:
			raise Exception("There have been previous parsing errors!")

		while self.__argsPos < len(self.programArgs):
			nextCmdCandidate = self.programArgs[self.__argsPos]
			cmd = self.__commands.get(nextCmdCandidate, None)
			if cmd is None:
				self.__bError = True
				raise Exception("Unknown command: \"" + nextCmdCandidate + "\"")
			self.__argsPos += 1

			if self.__argsPos + len(cmd.optionParameters) > len(self.programArgs):
				self.__bError = True
				raise Exception("Option " + cmd.name + " expects " + str(len(cmd.optionParameters)) + " arguments!")

			optionArgs = []
			for i in range(0, len(cmd.optionParameters)):
				optionArgs.append(cmd.optionParameters[i].parse(self.programArgs[self.__argsPos + i]))
			self.__argsPos += len(cmd.optionParameters)

			yield (cmd.name, optionArgs)
	#
	"""

	def parseCommands(self) -> typing.Iterable[NextCommand]:
		while True:
			ret = self.parseNextCommand()
			if ret.cmdName is None:
				break
			yield ret
	#

#









