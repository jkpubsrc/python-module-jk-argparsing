


import os
import sys
import typing
import operator

import jk_terminal_essentials

from ..ArgOption import ArgOption
from ..ArgCommand import ArgCommand
from ..textmodel.VisSettings import VisSettings
from ..textprimitives import *
from ..textmodel import *
from .ImplementationErrorException import ImplementationErrorException
from .HelpTextData import HelpTextData




class HelpTextBuilder(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self,
			options:typing.List[ArgOption],
			commands:typing.Dict[str,ArgCommand],
			commandsExtra:typing.Dict[str,ArgCommand],
			visSettings:VisSettings,
			helpTextData:HelpTextData,
		):

		# variables

		self.__options = options
		self.__commands = commands
		self.__commandsExtra = commandsExtra
		self.__visSettings = visSettings
		self.__helpTextData = helpTextData
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def ____makeDescr(self,
			description:str,
			supportsOptions:typing.List[ArgOption] = None,
			providedByCommands:typing.List[str] = None,
		) -> TextBlockSequence:

		tbDescrLines:typing.List[TextBlock] = []

		for line in description.strip().split("\n"):
			tbDescrLines.append(TextBlock(0, line))

		if supportsOptions:
			tbDescrLines.append(TextBlock(0, "Supported options: " + ", ".join([
				(("--" + o.longName) if o.longName else ("-" + o.shortName)) \
				for o in supportsOptions
			])))

		if providedByCommands:
			tbDescrLines.append(
				TextBlock(0, "Commands using this option: " + ", ".join(providedByCommands))
			)

		return TextBlockSequence(0, 0, tbDescrLines)
	#

	def ____windowWidth(self) -> int:
		try:
			sz = jk_terminal_essentials.getTerminalSize()
			return min(sz.columns - 1, 140)
		except:
			return 160
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	def __convertTSection(self, v:VisSettings, chapter:TSection) -> ITextBlock:
		assert isinstance(v, VisSettings)
		assert isinstance(chapter, TSection)

		# ----

		sec = TextBlockSequence(0, 0)

		sec.addBlock(TextBlock(v.title2_indent, chapter.title, v.title2_fgColor))
		sec.addBlock(TextEmpty(v.title2_paddingAfterTitle))

		for block in chapter.contentBlocks:
			sec.addBlock(TextBlock(v.section2_indent, block.text))
			sec.addBlock(TextEmpty(v.section2_gapBetweenSections))

		return sec
	#

	def __appendTitle1WithGap(self, v:VisSettings, title:str, ret:TextBlockSequence):
		assert isinstance(v, VisSettings)
		assert isinstance(title, str)
		assert isinstance(ret, TextBlockSequence)

		# ----

		ret.addBlock(TextBlock(v.title1_indent, v.title1_preprocessor(title) if v.title1_preprocessor else title, v.title1_fgColor))
		ret.addBlock(TextEmpty(v.title1_paddingAfterTitle))
	#

	def _txtCreateName(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		return TextBlock(0, self.__helpTextData.appName + " - " + self.__helpTextData.shortAppDescription, v.appName_fgColor)
	#

	def _txtCreateSynopsis(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__helpTextData.synopsisList:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Synopsis", ret)

		# content
		for synopsisText in self.__helpTextData.synopsisList:
			ret.addBlock(TextBlock(v.section1_indent, synopsisText, None))

		return ret
	#

	#### Done
	def _txtCreateOptions(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__options:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Options", ret)

		# content
		grid = TextGridBlock(v.section1_indent, v.options_tableRowGap, v.options_tableColumnsGap, columnLayouterL2R)
		ret.addBlock(grid)
		for o in self.__options:
			if o.isProvidedByCommand and not o.providedByCommands:
				# skip as this is a command option that is unused
				continue

			if o.shortName is not None:
				sShortName = "-" + o.shortName
				for op in o.optionParameters:
					sShortName += " " + op.displayName
			else:
				sShortName = ""

			if o.longName is not None:
				sLongName = "--" + o.longName
				for op in o.optionParameters:
					sLongName += " <{}>".format(op.displayName)
			else:
				sLongName = ""

			rows = [
				TextBlock(0, sShortName, v.options_fgColor),
				TextBlock(0, sLongName, v.options_fgColor),
				self.____makeDescr(o.description, providedByCommands=o.providedByCommands)
			]

			grid.addRow(rows)

		return ret
	#

	def _txtCreateAuthors(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__helpTextData.authorsList:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Authors", ret)

		# content
		for (name, email, description) in self.__helpTextData.authorsList:
			s = name
			if email:
				s += " <" + email + ">"
			if description:
				s += " - " + description
			ret.addBlock(TextBlock(v.section1_indent, s))

		return ret
	#

	def _txtReturnCodes(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__helpTextData.returnCodesList:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Program Exit Codes", ret)

		# content
		grid = TextGridBlock(v.section1_indent, v.exitCodes_tableRowGap, v.exitCodes_tableColumnsGap, columnLayouterL2R)
		ret.addBlock(grid)

		_returnCodesList = list(self.__helpTextData.returnCodesList)
		_returnCodesList.sort(key=operator.itemgetter(0))

		_prevRetCode:int = None
		for (retCode, retCodeDescription) in _returnCodesList:
			_s = "" if retCode == _prevRetCode else str(retCode)
			grid.addRow([
				TextBlock(0, _s, v.exitCodes_fgColor),
				TextBlock(0, retCodeDescription),
			])
			_prevRetCode = retCode

		return ret
	#

	#### DONE
	def _txtCreateCommands(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__commands:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, self.__helpTextData.titleCommandsStd, ret)

		# content
		grid = TextGridBlock(v.section1_indent, v.commands_tableRowGap, v.commands_tableColumnsGap, columnLayouterL2R)
		ret.addBlock(grid)
		keys = list(self.__commands.keys())
		keys.sort()
		for key in keys:
			cmd = self.__commands[key]

			if cmd.isHidden:
				continue

			s = cmd.name
			for op in cmd.optionParameters:
				s += " <{}>".format(op.displayName)

			grid.addRow([
				TextBlock(0, s, v.commands_fgColor),
				self.____makeDescr(cmd.description, supportsOptions=cmd.supportsOptions)
			])

		return ret
	#

	#### DONE
	def _txtCreateExtraCommands(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__commandsExtra:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, self.__helpTextData.titleCommandsExtra, ret)

		# content
		grid = TextGridBlock(v.section1_indent, v.commands_tableRowGap, v.commands_tableColumnsGap, columnLayouterL2R)
		ret.addBlock(grid)
		keys = list(self.__commandsExtra.keys())
		keys.sort()
		for key in keys:
			cmd = self.__commandsExtra[key]

			if cmd.isHidden:
				continue

			s = cmd.name
			for op in cmd.optionParameters:
				s += " <{}>".format(op.displayName)

			grid.addRow([
				TextBlock(0, s, v.commands_fgColor),
				self.____makeDescr(cmd.description, supportsOptions=cmd.supportsOptions)
			])

		return ret
	#

	def _txtCreateLicense(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__helpTextData.licenseTextLines:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "License", ret)

		# content
		for line in self.__helpTextData.licenseTextLines:
			ret.addBlock(TextBlock(v.section1_indent, line))
			ret.addBlock(TextEmpty(v.section2_gapBetweenSections))

		return ret
	#

	def _txtCreateDescription(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		if not self.__helpTextData.descriptionChapters:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Description", ret)

		# content
		for chapter in self.__helpTextData.descriptionChapters:
			if isinstance(chapter, TBlock):
				ret.addBlock(TextBlock(v.section1_indent, chapter.text))
				ret.addBlock(TextEmpty(v.section2_gapBetweenSections))
			elif isinstance(chapter, TSection):
				ret.addBlock(self.__convertTSection(v, chapter))
			else:
				raise ImplementationErrorException()

		return ret
	#

	def _txtCreateExtraHead(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		# TODO: methods are almost identical: _txtCreateExtraHead(), _txtCreateExtraMiddle() and _txtCreateExtraHead()

		if not self.__helpTextData.extraHeadChapters:
			return None

		ret = TextBlockSequence(0, 0)

		for n, chapter in enumerate(self.__helpTextData.extraHeadChapters):
			assert isinstance(chapter, TSection)

			if n > 0:
				ret.addBlock(TextEmpty(v.section1_gapBetweenSections))

			# title
			self.__appendTitle1WithGap(v, chapter.title, ret)

			# content
			bNeedGap = False
			for sub in chapter.contentBlocks:
				if bNeedGap:
					ret.addBlock(TextEmpty(v.section2_gapBetweenSections))
					bNeedGap = False
				if isinstance(sub, TSection):
					ret.addBlock(self.__convertTSection(v, sub))
				elif isinstance(sub, TBlock):
					ret.addBlock(TextBlock(v.section1_indent, sub.text))
					bNeedGap = True
				elif isinstance(sub, TList):
					for item in sub.items:
						ret.addBlock(TextBlock(v.section1_indent, item, listIndent=v.listIndent, listChar=v.listChar))
					bNeedGap = True
				else:
					raise ImplementationErrorException()

		return ret
	#

	def _txtCreateExtraMiddle(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		# TODO: methods are almost identical: _txtCreateExtraHead(), _txtCreateExtraMiddle() and _txtCreateExtraHead()

		if not self.__helpTextData.extraMiddleChapters:
			return None

		ret = TextBlockSequence(0, 0)

		for n, chapter in enumerate(self.__helpTextData.extraMiddleChapters):
			assert isinstance(chapter, TSection)

			if n > 0:
				ret.addBlock(TextEmpty(v.section1_gapBetweenSections))

			# title
			self.__appendTitle1WithGap(v, chapter.title, ret)

			# content
			bNeedGap = False
			for sub in chapter.contentBlocks:
				if bNeedGap:
					ret.addBlock(TextEmpty(v.section2_gapBetweenSections))
					bNeedGap = False
				if isinstance(sub, TSection):
					ret.addBlock(self.__convertTSection(v, sub))
				elif isinstance(sub, TBlock):
					ret.addBlock(TextBlock(v.section1_indent, sub.text))
					bNeedGap = True
				elif isinstance(sub, TList):
					for item in sub.items:
						ret.addBlock(TextBlock(v.section1_indent, item, listIndent=v.listIndent, listChar=v.listChar))
					bNeedGap = True
				else:
					raise ImplementationErrorException()

		return ret
	#

	def _txtCreateExtraEnd(self, v:VisSettings) -> ITextBlock:
		assert isinstance(v, VisSettings)

		# ----

		# TODO: methods are almost identical: _txtCreateExtraHead(), _txtCreateExtraMiddle() and _txtCreateExtraHead()

		if not self.__helpTextData.extraEndChapters:
			return None

		ret = TextBlockSequence(0, 0)

		for n, chapter in enumerate(self.__helpTextData.extraEndChapters):
			assert isinstance(chapter, TSection)

			if n > 0:
				ret.addBlock(TextEmpty(v.section1_gapBetweenSections))

			# title
			self.__appendTitle1WithGap(v, chapter.title, ret)

			# content
			bNeedGap = False
			for sub in chapter.contentBlocks:
				if bNeedGap:
					ret.addBlock(TextEmpty(v.section2_gapBetweenSections))
					bNeedGap = False
				if isinstance(sub, TSection):
					ret.addBlock(self.__convertTSection(v, sub))
				elif isinstance(sub, TBlock):
					ret.addBlock(TextBlock(v.section1_indent, sub.text))
					bNeedGap = True
				elif isinstance(sub, TList):
					for item in sub.items:
						ret.addBlock(TextBlock(v.section1_indent, item, listIndent=v.listIndent, listChar=v.listChar))
					bNeedGap = True
				else:
					raise ImplementationErrorException()

		return ret
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def buildHelpText(self, bColor:bool = None) -> typing.List[str]:
		if bColor is None:
			bColor = jk_terminal_essentials.checkTerminalSupportsColors()

		v = self.__visSettings
		doc = TextBlockSequence(0, v.section1_gapBetweenSections)

		# ----

		for provider in [
				self._txtCreateName,
				self._txtCreateSynopsis,
				self._txtCreateExtraHead,
				self._txtCreateDescription,
				self._txtCreateExtraMiddle,
				self._txtCreateOptions,
				self._txtCreateCommands,
				self._txtCreateExtraCommands,
				self._txtCreateExtraEnd,
				self._txtReturnCodes,
				self._txtCreateAuthors,
				self._txtCreateLicense,
			]:

			x = provider(v)
			if x:
				doc.addBlock(x)

		# ----

		doc.layout(self.____windowWidth())
		return [ str(x) for x in doc.getLines(bColor) ]
	#

#






