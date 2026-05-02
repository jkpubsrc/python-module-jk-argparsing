

import jk_terminal_essentials







class VisSettings(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		self.appName_fgColor = jk_terminal_essentials.FGCOLOR_LIGHT_YELLOW

		self.title1_fgColor = jk_terminal_essentials.FGCOLOR_LIGHT_CYAN
		self.title1_preprocessor = str.upper
		self.title1_indent = 0
		self.title1_paddingAfterTitle = 1

		self.listIndent = 2
		self.listChar = "-"

		self.section1_indent = 4
		# the vertical distance between blocks on level 1
		self.section1_gapBetweenSections = 1

		self.title2_fgColor = jk_terminal_essentials.FGCOLOR_WHITE
		self.title2_preprocessor = None
		self.title2_indent = 4
		self.title2_paddingAfterTitle = 1

		self.section2_indent = 8
		# the vertical distance between blocks on level 2
		self.section2_gapBetweenSections = 1

		self.options_fgColor = jk_terminal_essentials.FGCOLOR_LIGHT_BLUE
		self.options_tableColumnsGap = 2
		self.options_tableRowGap = 0

		self.exitCodes_fgColor = jk_terminal_essentials.FGCOLOR_LIGHT_BLUE
		self.exitCodes_tableColumnsGap = 2
		self.exitCodes_tableRowGap = 0

		self.envVars_fgColor = jk_terminal_essentials.FGCOLOR_LIGHT_BLUE
		self.envVars_tableColumnsGap = 2
		self.envVars_tableRowGap = 0

		self.commands_fgColor = jk_terminal_essentials.FGCOLOR_LIGHT_BLUE
		self.commands_tableColumnsGap = 2
		self.commands_tableRowGap = 0
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#






