


import typing




class LicenseInfo(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			bIsFreeSoftware:bool = None,
			bIsNamedLicense:bool = None,
			shortLicenseName:str = None,
			longLicenseName:str = None,
			licenseCopyrightOwner:str = None,
			versions:str = None,
			url:str = None,
			fullText:list[str] = None,
			shortAltNames:list[str] = None,
		):

		assert isinstance(bIsFreeSoftware, bool)
		assert isinstance(bIsNamedLicense, bool)
		assert isinstance(shortLicenseName, str)
		if bIsNamedLicense:
			assert isinstance(longLicenseName, str)
		if bIsNamedLicense:
			assert isinstance(licenseCopyrightOwner, str)
		if versions is not None:
			assert isinstance(versions, str)
		if url is not None:
			assert isinstance(url, str)
		if fullText is not None:
			assert isinstance(fullText, list)
			for s in fullText:
				assert isinstance(s, str)
		if shortAltNames is not None:
			assert isinstance(shortAltNames, list)
			for s in shortAltNames:
				assert isinstance(s, str)

		# ----

		self.isNamedLicense = bIsNamedLicense or bIsFreeSoftware
		self.isFreeSoftware = bIsFreeSoftware
		self.id = shortLicenseName.lower()
		self.shortLicenseName = shortLicenseName
		self.longLicenseName = longLicenseName
		self.licenseCopyrightOwner = licenseCopyrightOwner
		self.url = url
		self.newerVersionsAllowed = False
		if versions is None:
			self.version = None
		else:
			if versions.endswith("+"):
				self.newerVersionsAllowed = True
				versions = versions[:-1]
			self.version = int(versions)
		self.fullText = fullText

		self.shortAltNames = shortAltNames
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __tostr(self, data):
		if isinstance(data, (tuple, list)):
			if len(data) == 0:
				return ""
			elif (len(data) == 2) and isinstance(data[0], int) and isinstance(data[1], int):
				return str(data[0]) + "-" + str(data[1])
			else:
				return ", ".join([ str(d) for d in data ])
		else:
			return str(data)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def toString(self, **kwargs) -> list[str]:
		ret:list[str] = []

		sb = ""

		if self.isFreeSoftware:
			sb += "This program is free software: you can redistribute it and/or modify it under the terms of the "
			sb += self.longLicenseName
		elif self.isNamedLicense:
			sb += "This program is distributed under the terms of the "
			sb += self.longLicenseName

		if self.isNamedLicense:
			sb += " as published by " + self.licenseCopyrightOwner

		if (self.version is not None) and (self.version > 0):
			if self.newerVersionsAllowed:
				sb += " either version " + str(self.version) + " or later."
			else:
				sb += " in version " + str(self.version) + "."
		elif self.isNamedLicense:
			sb += "."

		if self.fullText is None:
			if (self.url is not None) and (self.longLicenseName is not None):
				sb += " For more details see the " + self.longLicenseName + ", which should be vailable at: "
				sb += self.url

		if sb:
			ret.append(sb)

		if self.fullText is not None:
			textLines = self.fullText
			for key in kwargs:
				value = kwargs[key]
				skey = "{{$" + key + "}}"
				for i in range(0, len(textLines)):
					curlen = -1
					while True:
						curlen = len(textLines[i])
						textLines[i] = textLines[i].replace(skey, self.__tostr(value))
						if len(textLines[i]) == curlen:
							break
			ret.extend(textLines)

		return ret
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#



