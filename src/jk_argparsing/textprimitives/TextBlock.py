


from .XLineFragment import XLineFragment
from .ITextBlock import ITextBlock





_RESET = "\x1b[0m"





#
# Instances of this class represent a block of text. This is typically a paragraph.
#
class TextBlock(ITextBlock):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, indent:int, paragraphText:str, color:str = None, listIndent:int = None, listChar:str = None):
		assert isinstance(indent, int)
		assert isinstance(paragraphText, str)
		if color is not None:
			assert isinstance(color, str)
		if listIndent is not None:
			assert isinstance(listIndent, int)
			assert listIndent > 0
		if listChar is not None:
			assert isinstance(listChar, str)
			assert len(listChar) == 1
			assert listIndent is not None

		# ----

		self.__minTextWidth = 0				# the minimum width calculated by the minimum word length
		self.__wordTokens = []				# stores tuples: word length, word
		self.__indent = indent				# the indentation
		self.__preferredWidth = None
		self.__maxTextWidth = 0				# this will receive the width required for the whole text to be in a single line
		self.__listIndent = 0
		self.__listPrefix = None

		if listChar is not None:
			self.__listIndent = listIndent
			self.__listPrefix = listChar + " " * (listIndent - 1)

		paragraphText = paragraphText.strip()
		if paragraphText:
			self.__wordTokens = []
			self.__maxTextWidth = -1
			for w in paragraphText.split(" "):
				if w:
					wlen = len(w)
					self.__wordTokens.append((wlen, w))
					self.__maxTextWidth += wlen + 1
					if wlen > self.__minTextWidth:
						self.__minTextWidth = wlen
		# colorize everything (or not)
		self.__color = color if color else ""
	#

	################################################################################################################################
	## Properties
	################################################################################################################################

	#
	# The preferred with including the indentation
	#
	@property
	def preferredWidth(self) -> int:
		if self.__preferredWidth is None:
			return self.__indent + self.__maxTextWidth + self.__listIndent

		return self.__preferredWidth
	#

	"""
	#
	# Set the preferred with including the indentation
	#
	@preferredWidth.setter
	def preferredWidth(self, w:int):
		assert isinstance(w, int)
		w -= self.__indent
		if w > self.__maxTextWidth:
			w = self.__maxTextWidth
		if w < self.__minTextWidth:
			w = self.__minTextWidth
		self.__preferredWidth = self.__indent + w
	#
	"""

	@property
	def maxWidth(self) -> int:
		return self.__indent + self.__maxTextWidth
	#

	@property
	def minWidth(self) -> int:
		return self.__indent + self.__minTextWidth
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# Emits lines
	#
	def __generateLines(self, bColor:bool):
		# calculate the layouting width available
		nAvailableWidth = self.preferredWidth - self.__indent - self.__listIndent

		# layout lines

		lineBuffer = []
		currentLen = 0
		bIsFirstLineFragment = True
		for wlen, w in self.__wordTokens:
			expectedLengthAfterAppend = currentLen + (len(lineBuffer) > 0) + wlen
			if lineBuffer and (expectedLengthAfterAppend > nAvailableWidth):
				# emit existing data
				s = " ".join(lineBuffer)
				lenS = len(s)
				if bColor and self.__color:
					s = self.__color + s + _RESET
				if bIsFirstLineFragment and (self.__listIndent > 0):
					yield XLineFragment(self.__indent, self.__listPrefix + s, lenS)
				else:
					yield XLineFragment(self.__indent + self.__listIndent, s, lenS)
				bIsFirstLineFragment = False
				# clear buffer
				lineBuffer.clear()
				# prepare append
				expectedLengthAfterAppend = wlen

			# append to buffer
			lineBuffer.append(w)
			currentLen = expectedLengthAfterAppend

		if lineBuffer:
			# emit existing data
			s = " ".join(lineBuffer)
			lenS = len(s)
			if bColor and self.__color:
				s = self.__color + s + _RESET
			if bIsFirstLineFragment and (self.__listIndent > 0):
				yield XLineFragment(self.__indent, self.__listPrefix + s, lenS)
			else:
				yield XLineFragment(self.__indent + self.__listIndent, s, lenS)
			bIsFirstLineFragment = False
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def layout(self, availableWidth:int):
		self.__preferredWidth = availableWidth
	#

	#
	# @return		XLineFragment[]		Returns a list of lines.
	#
	def getLines(self, bColor:bool) -> list:
		return list(self.__generateLines(bColor))
	#

#



