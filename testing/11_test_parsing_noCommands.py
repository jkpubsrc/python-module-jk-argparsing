

import jk_logging
import jk_assert

import jk_argparsing




with jk_logging.wrapMain() as log:

	# ---- definition

	ap = jk_argparsing.ArgsParser("foobar", "Lorem ipsum dolor sid amet")

	ap.createOption("h", "help", "Display a help page")
	ap.createOption("l", None, "long").onOption = \
		lambda argOption, argOptionArguments, parsedArgs: \
			parsedArgs.optionData.set("long", True)
	ap.createOption("a", None, "all").onOption = \
		lambda argOption, argOptionArguments, parsedArgs: \
			parsedArgs.optionData.set("all", True)

	ap.noCommand() \
		.expectString(
			displayName="aStr",
		)

	# ---- parse

	parsedArgs = ap.parse([
		"-la",
		"something",
	])

	parsedArgs.dump()

	# ---- verify options

	jk_assert.assertEquals(parsedArgs.optionData, {
		"long": True,
		"all": True,
	})

	# ---- verfiy commands

	jk_assert.assertEquals(parsedArgs.terminate, False)
	jk_assert.assertEquals(parsedArgs.programArgs, [
		"something",
	])

	programArgs = list(parsedArgs.parseNoCommand())
	print("programArgs:", programArgs)

	assert len(programArgs) == 1
	assert programArgs[0] == "something"
#



