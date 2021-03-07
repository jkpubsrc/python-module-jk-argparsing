


import typing



from .ArgsOptionDataDict import ArgsOptionDataDict





#
# This class contains the results of command line parsing.
#
class ParsedArgs(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, commands):
		self.__commands = commands
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
	def optionData(self):
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

	def parseNextCommand(self):
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

#









