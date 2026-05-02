


import typing
import operator

import jk_terminal_essentials

from jk_argparsing_textprimitive import *

from ..ex.ImplementationErrorException import ImplementationErrorException
from ..ArgOption import ArgOption
from ..ArgCommand import ArgCommand
from ..textmodel.TBlock import TBlock
from ..textmodel.TList import TList
from ..textmodel.TSection import TSection
from .VisSettings import VisSettings
from .HelpTextSrcData import HelpTextSrcData
from .IHelpTextBuilder import IHelpTextBuilder






class ConsoleHelpTextBuilder(IHelpTextBuilder):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		pass
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
			return max(sz.columns - 1, 140)
		except:
			return 160
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	def __convertTSection(self, v:VisSettings, chapter:TSection) -> ITextBlock:
		assert isinstance(v, VisSettings)
		assert isinstance(chapter, TSection)

		# ----

		sec = TextBlockSequence(0, 0)

		sec.addBlock(
			TextBlock(
				v.title2_indent,
				v.title2_preprocessor(chapter.title) if v.title2_preprocessor else chapter.title,
				v.title2_fgColor,
				semanticTypeID="h2",
			)
		)
		sec.addBlock(TextEmpty(v.title2_paddingAfterTitle))

		for block in chapter.contentBlocks:
			sec.addBlock(TextBlock(v.section2_indent, block.text, "p"))
			sec.addBlock(TextEmpty(v.section2_gapBetweenSections))

		return sec
	#

	def __appendTitle1WithGap(self, v:VisSettings, title:str, ret:TextBlockSequence):
		assert isinstance(v, VisSettings)
		assert isinstance(title, str)
		assert isinstance(ret, TextBlockSequence)

		# ----

		ret.addBlock(
			TextBlock(
				v.title1_indent,
				v.title1_preprocessor(title) if v.title1_preprocessor else title,
				v.title1_fgColor,
				semanticTypeID="h1",
			)
		)

		ret.addBlock(
			TextEmpty(
				v.title1_paddingAfterTitle,
				semanticTypeID="gap",
			)
		)
	#

	def _txtCreateAppName(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		return TextBlock(0, ctx.appName + " - " + ctx.shortAppDescription, v.appName_fgColor, semanticTypeID="app")
	#

	def _txtCreateSynopsis(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.synopsisList:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Synopsis", ret)

		# content
		for synopsisText in ctx.synopsisList:
			ret.addBlock(TextBlock(v.section1_indent, synopsisText, None, semanticTypeID="p"))

		return ret
	#

	def _txtCreateOptions(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.options:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Options", ret)

		# content
		grid = TextGridBlock(v.section1_indent, 3, v.options_tableRowGap, v.options_tableColumnsGap)
		grid.columns[0].columnWrapMode = EnumWrapMode.NO_WRAP
		grid.columns[1].columnWrapMode = EnumWrapMode.NO_WRAP
		ret.addBlock(grid)
		for o in ctx.options:
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

			cells = [
				TextBlock(0, sShortName, v.options_fgColor),
				TextBlock(0, sLongName, v.options_fgColor),
				self.____makeDescr(o.description, providedByCommands=o.providedByCommands),
			]

			grid.addRow(cells)

		return ret
	#

	def _txtCreateAuthors(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.authorsList:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Authors", ret)

		# content
		for (name, email, description) in ctx.authorsList:
			s = name
			if email:
				s += " <" + email + ">"
			if description:
				s += " - " + description
			ret.addBlock(TextBlock(v.section1_indent, s))

		return ret
	#

	def _txtReturnCodes(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.returnCodesList:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Program Exit Codes", ret)

		# content
		grid = TextGridBlock(v.section1_indent, 2, v.exitCodes_tableRowGap, v.exitCodes_tableColumnsGap)
		grid.columns[0].columnWrapMode = EnumWrapMode.NO_WRAP
		ret.addBlock(grid)

		_returnCodesList = list(ctx.returnCodesList)
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

	def _txtEnvVars(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.envVarsList:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Environment Variables", ret)

		# content
		grid = TextGridBlock(v.section1_indent, 2, v.envVars_tableRowGap, v.envVars_tableColumnsGap)
		grid.columns[0].columnWrapMode = EnumWrapMode.NO_WRAP
		ret.addBlock(grid)

		_envsList = list(ctx.envVarsList)
		_envsList.sort(key=operator.itemgetter(0))

		_prevEnvVarName:str|None = None
		for (envVarName, envVarDescription) in _envsList:
			_s = "" if envVarName == _prevEnvVarName else str(envVarName)
			grid.addRow([
				TextBlock(0, _s, v.envVars_fgColor),
				TextBlock(0, envVarDescription),
			])
			_prevEnvVarName = envVarName

		return ret
	#

	def _txtCreateCommands(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.commands:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, ctx.titleCommandsStd, ret)

		# content
		grid = TextGridBlock(v.section1_indent, 2, v.commands_tableRowGap, v.commands_tableColumnsGap)
		grid.columns[0].columnWrapMode = EnumWrapMode.NO_WRAP
		ret.addBlock(grid)
		keys = list(ctx.commands.keys())
		keys.sort()
		for key in keys:
			cmd = ctx.commands[key]

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

	def _txtCreateHiddenCommands(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.commands:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, ctx.titleCommandsHidden, ret)

		# content
		grid = TextGridBlock(v.section1_indent, 2, v.commands_tableRowGap, v.commands_tableColumnsGap)
		grid.columns[0].columnWrapMode = EnumWrapMode.NO_WRAP
		ret.addBlock(grid)
		keys = list(ctx.commands.keys())
		keys.sort()
		for key in keys:
			cmd = ctx.commands[key]

			if not cmd.isHidden:
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

	def _txtCreateExtraCommands(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.commandsExtra:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, ctx.titleCommandsExtra, ret)

		# content
		grid = TextGridBlock(v.section1_indent, 2, v.commands_tableRowGap, v.commands_tableColumnsGap)
		grid.columns[0].columnWrapMode = EnumWrapMode.NO_WRAP
		ret.addBlock(grid)
		keys = list(ctx.commandsExtra.keys())
		keys.sort()
		for key in keys:
			cmd = ctx.commandsExtra[key]

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

	def _txtCreateLicense(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.licenseTextLines:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "License", ret)

		# content
		for line in ctx.licenseTextLines:
			ret.addBlock(TextBlock(v.section1_indent, line))
			ret.addBlock(TextEmpty(v.section2_gapBetweenSections))

		return ret
	#

	def _txtCreateDescription(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		if not ctx.descriptionChapters:
			return None

		ret = TextBlockSequence(0, 0)

		# title
		self.__appendTitle1WithGap(v, "Description", ret)

		# content
		for chapter in ctx.descriptionChapters:
			if isinstance(chapter, TBlock):
				ret.addBlock(TextBlock(v.section1_indent, chapter.text))
				ret.addBlock(TextEmpty(v.section2_gapBetweenSections))
			elif isinstance(chapter, TSection):
				ret.addBlock(self.__convertTSection(v, chapter))
			else:
				raise ImplementationErrorException()

		return ret
	#

	def _txtCreateExtraHead(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		# TODO: methods are almost identical: _txtCreateExtraHead(), _txtCreateExtraMiddle() and _txtCreateExtraHead()

		if not ctx.extraHeadChapters:
			return None

		ret = TextBlockSequence(0, 0)

		for n, chapter in enumerate(ctx.extraHeadChapters):
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

	def _txtCreateExtraMiddle(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		# TODO: methods are almost identical: _txtCreateExtraHead(), _txtCreateExtraMiddle() and _txtCreateExtraHead()

		if not ctx.extraMiddleChapters:
			return None

		ret = TextBlockSequence(0, 0)

		for n, chapter in enumerate(ctx.extraMiddleChapters):
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

	def _txtCreateExtraEnd(self,
			ctx:HelpTextSrcData,
		) -> ITextBlock|None:
		assert isinstance(ctx, HelpTextSrcData)
		v = ctx.visSettings

		# ----

		# TODO: methods are almost identical: _txtCreateExtraHead(), _txtCreateExtraMiddle() and _txtCreateExtraHead()

		if not ctx.extraEndChapters:
			return None

		ret = TextBlockSequence(0, 0)

		for n, chapter in enumerate(ctx.extraEndChapters):
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

	def buildHelpText(self,
			ctx:HelpTextSrcData,
			bColor:bool|None = None,
			bShowHiddenCmds:bool = False,
			**kwargs,
		) -> list[str]:

		if bColor is None:
			bColor = jk_terminal_essentials.checkTerminalSupportsColors()

		v = ctx.visSettings

		# ----

		doc = TextBlockSequence(0, v.section1_gapBetweenSections)

		# ----

		providers = [
			self._txtCreateAppName,
			self._txtCreateSynopsis,
			self._txtCreateExtraHead,
			self._txtCreateDescription,
			self._txtCreateExtraMiddle,
			self._txtCreateOptions,
			self._txtCreateCommands,
			self._txtCreateExtraCommands,
		]

		if bShowHiddenCmds:
			providers.append(self._txtCreateHiddenCommands)

		providers.extend([
			self._txtCreateExtraEnd,
			self._txtEnvVars,
			self._txtReturnCodes,
			self._txtCreateAuthors,
			self._txtCreateLicense,
		])

		# ----

		for provider in providers:
			x = provider(ctx)
			if x:
				doc.addBlock(x)

		# ----

		doc.layout(self.____windowWidth())
		return [ str(x) for x in doc.getLines(bColor) ]
	#

#






