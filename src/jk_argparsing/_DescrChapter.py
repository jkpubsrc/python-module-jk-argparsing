


from ._DescrPargraph import _DescrPargraph




class _DescrChapter(object):

	def __init__(self, chapterName:str, paragraphs:list):
		if chapterName:
			self.__chapterName = _DescrPargraph(chapterName)
		else:
			self.__chapterName = None

		assert paragraphs
		self.__paragraphs = [
			_DescrPargraph(p) for p in paragraphs
		]
	#

	def toLines(self, prefix:str, maxWidth:int) -> list:
		if prefix is None:
			prefix = ""
		else:
			assert isinstance(prefix, str)

		assert isinstance(maxWidth, int)
		assert maxWidth > 0

		ret = []

		if self.__chapterName:
			ret.extend(self.__chapterName.toLines(prefix, maxWidth))
			ret.append("")
			prefix = "  " + prefix
			maxWidth -= 2

		bAddEmptyLine = False
		for p in self.__paragraphs:
			if bAddEmptyLine:
				ret.append("")
			ret.extend(p.toLines(prefix, maxWidth))
			bAddEmptyLine = True

		return ret
	#

#












