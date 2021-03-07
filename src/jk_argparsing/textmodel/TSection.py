


import typing

from .TBlock import TBlock





class TSection(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, title:str, contentBlocks:typing.Sequence):
		assert isinstance(title, str)
		assert title
		self.__title = title

		self.__contentBlocks = []
		if contentBlocks:
			if isinstance(contentBlocks, str):
				raise TypeError(str(type(contentBlocks)))
			for content in contentBlocks:
				self.addContentBlock(content)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def title(self) -> str:
		return self.__title
	#

	@property
	def contentBlocks(self) -> list:
		return list(self.__contentBlocks)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def addContentBlock(self, content:typing.Union[str,TBlock]):
		b = None
		if isinstance(content, TBlock):
			b = content
		elif isinstance(content, TSection):
			b = content
		elif isinstance(content, str):
			b = TBlock(content)
		else:
			raise Exception("Unknown data type used for content: " + type(content).__name__)
		self.__contentBlocks.append(b)
	#

#













