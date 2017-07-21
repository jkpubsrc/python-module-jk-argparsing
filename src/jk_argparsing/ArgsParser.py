#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc
import re

import sh

from .ArgOption import ArgOption
from .ParsedArgs import ParsedArgs
from .ArgsOptionDataDict import ArgsOptionDataDict
from .ArgUtils import ArgUtils
from .AvailableLicenseList import AvailableLicenseList
from .ArgCommand import ArgCommand





class ArgsParser(object):

	class _TextTableRow2(object):

		def __init__(self, col1, col2):
			self.col1 = col1
			self.col2 = col2

	#



	class _TextTableRow3(object):

		def __init__(self, col1, col2, col3):
			self.col1 = col1
			self.col2 = col2
			self.col3 = col3

	#



	class _TextTable2(object):

		def __init__(self):
			self.__rows = []

		def addRow(self, col1, col2):
			assert isinstance(col1, str)
			assert isinstance(col2, str)

			self.__rows.append(ArgsParser._TextTableRow2(col1, col2))

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



	class _TextTable3(object):

		def __init__(self):
			self.__rows = []

		def addRow(self, col1, col2, col3):
			assert isinstance(col1, str)
			assert isinstance(col2, str)
			assert isinstance(col3, str)

			self.__rows.append(ArgsParser._TextTableRow3(col1, col2, col3))

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



	def __init__(self, appName, shortAppDescription):
		assert isinstance(appName, str)
		assert isinstance(shortAppDescription, str)

		self.__commands = {}
		self.__longArgs = {}
		self.__shortArgs = {}
		self.__options = []
		self.__authors = []
		self.__returnCodes = []
		self.__appName = appName
		self.__shortAppDescription = shortAppDescription
		self.__appName = appName
		self.__optionDataDefaults = ArgsOptionDataDict()
		self.__licenseTextLines = None




	@property
	def optionDataDefaults(self):
		return self.__optionDataDefaults



	@property
	def appName(self):
		return self.__appName



	@property
	def shortAppDescription(self):
		return self.__shortAppDescription



	def createCommand(self, name, description):
		assert isinstance(name, str)
		assert isinstance(description, str)

		o = ArgCommand(name, description)
		if o.name in self.__commands:
			raise Exception("A command named '-" + o.name + "' already exists!")
		self.__commands[o.name] = o

		return o



	def createOption(self, shortName, longName, description):
		if shortName != None:
			assert isinstance(shortName, str)
			assert len(shortName) == 1

		if longName != None:
			assert isinstance(longName, str)

		assert isinstance(description, str)

		if (shortName is None) and (longName is None):
			raise Exception("Arguments need at least a long or a short name!")

		o = ArgOption(shortName, longName, description)

		if shortName != None:
			if o.shortName in self.__shortArgs:
				raise Exception("A short argument named '-" + o.shortName + "' already exists!")
			self.__shortArgs[o.shortName] = o
		if longName != None:
			if o.longName in self.__longArgs:
				raise Exception("A long argument named '-" + o.longName + "' already exists!")
			self.__longArgs[o.longName] = o

		self.__options.append(o)

		return o



	def showHelp(self):
		for line in self.buildHelpText():
			print(line)
		print()



	def __windowWidth(self):
		try:
			sz = os.get_terminal_size()
			return sz.columns - 1
		except:
			return 160



	def createAuthor(self, name, email = None):
		assert isinstance(name, str)
		if email != None:
			assert isinstance(email, str)

		self.__authors.append((name, email))

		return self



	def createReturnCode(self, returnCode, description):
		assert isinstance(returnCode, int)
		assert isinstance(description, str)

		self.__returnCodes.append((returnCode, description))

		return self



	def setLicense(self, licenseID, **kwargs):
		assert isinstance(licenseID, str)

		availableLicenseList = AvailableLicenseList()
		self.__licenseTextLines = availableLicenseList.getText(licenseID, **kwargs)
		if self.__licenseTextLines is None:
			raise Exception("No such license: " + licenseID)

		return self



	def buildHelpText(self):
		windowWidth = self.__windowWidth()
		ret = []

		ArgUtils.writePrefixedWrappingText(self.__appName + " - ", self.__shortAppDescription, windowWidth, ret)

		ret.append("")
		ret.append("  Options:")
		ret.append("")

		textTable = ArgsParser._TextTable3()
		for o in self.__options:
			sShortName = ("-" + o.shortName) if (o.shortName != None) else ""
			if o.longName != None:
				sLongName = "--" + o.longName
				for op in o.optionParameters:
					sLongName += " " + op.displayName
			else:
				sLongName = ""
			textTable.addRow(sShortName, sLongName, o.description)
		textTable.print(4, 2, windowWidth, ret)

		if len(self.__authors) > 0:
			ret.append("")
			if len(self.__authors) > 1:
				ret.append("  Authors:")
			else:
				ret.append("  Author:")
			ret.append("")

			for (name, email) in self.__authors:
				if email is None:
					ret.append("    " + name)
				else:
					ret.append("    " + name + " <" + email + ">")

		if len(self.__commands) > 0:
			ret.append("")
			ret.append("  Commands:")
			ret.append("")

			textTable = ArgsParser._TextTable2()
			keys = list(self.__commands.keys())
			keys.sort()
			for key in keys:
				cmd = self.__commands[key]
				s = cmd.name
				for op in cmd.optionParameters:
					s += " " + op.displayName
				textTable.addRow(s, cmd.description)
			textTable.print(4, 2, windowWidth, ret)

		if len(self.__returnCodes) > 0:
			ret.append("")
			ret.append("  Return codes:")
			ret.append("")

			textTable = ArgsParser._TextTable2()
			for (retCode, retCodeDescription) in self.__returnCodes:
				textTable.addRow(str(retCode), retCodeDescription)
			textTable.print(4, 2, windowWidth, ret)

		if (self.__licenseTextLines != None) and (len(self.__licenseTextLines) > 0):
			ret.append("")
			ret.append("  License:")

			for line in self.__licenseTextLines:
				ret.append("")
				ArgUtils.writePrefixedWrappingText("    ", line, windowWidth, ret)

		return ret



	def parse(self, args = None):
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

		optionsRequired = []	# List<ArgOption>()
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
							op = self.__eatShortOption(current[i], ret)
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



	def __eatLongOption(self, optionName, args, argsPos, ret):
		assert isinstance(optionName, str)
		assert isinstance(args, list)
		assert isinstance(argsPos, int)
		assert isinstance(ret, ParsedArgs)

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



	def __eatShortOption(self, optionName, ret):
		assert isinstance(optionName, str)
		assert isinstance(ret, ParsedArgs)

		o = self.__shortArgs.get(optionName, None)
		if o is None:
			raise Exception("No such option: " + optionName)

		o._invokeOpt(None, ret)

		return o









