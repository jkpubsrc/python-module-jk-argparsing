





class _DescrPargraph(object):

	def __init__(self, paragraph:str):
		assert isinstance(paragraph, str)

		self.__words = []
		for w in paragraph.split(" "):
			if w:
				self.__words.append(w)
	#

	def __generateLines(self, prefix:str, maxWidth:int):
		lineBuffer = []
		currentLen = 0
		for w in self.__words:
			expectedLengthAfterAppend = currentLen + (len(lineBuffer) > 0) + len(w)
			if lineBuffer and (expectedLengthAfterAppend >= maxWidth):
				yield prefix + " ".join(lineBuffer)
				lineBuffer.clear()
				lineBuffer.append(w)
				currentLen = len(w)
			else:
				lineBuffer.append(w)
				currentLen = expectedLengthAfterAppend

		if lineBuffer:
			yield prefix + " ".join(lineBuffer)
	#

	def toLines(self, prefix:str, maxWidth:int) -> list:
		if prefix is None:
			prefix = ""
		else:
			assert isinstance(prefix, str)

		assert isinstance(maxWidth, int)
		assert maxWidth > 0

		return list(self.__generateLines(prefix, maxWidth))
	#

#








