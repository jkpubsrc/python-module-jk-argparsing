#!/usr/bin/python3


import jk_logging
import jk_testing

import jk_argparsing




with jk_logging.wrapMain() as log:

	# ---- definition

	ap = jk_argparsing.ArgsParser("foobar", "Lorem ipsum dolor sid amet")

	# ----

	ap.createOption("h", "help", "Display a help page")

	ap.createOption(None, "parse-strlist", "Parse a string list") \
		.expectCommaSeparatedStringList(
			displayName="aStrList",
			listMinLength=1,
			strMinLength=3,
		).onOption = lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("aStrListValue", argOptionArguments[0])

	ap.createOption(None, "parse-bool", "Parse a boolean value") \
		.expectBoolean(
			displayName="aBool",
		).onOption = lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("aBool", argOptionArguments[0])

	ap.createOption(None, "parse-int", "Parse an integer value") \
		.expectInt32(
			displayName="anInt",
		).onOption = lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("anInt", argOptionArguments[0])
	
	# ----

	cmdBool = ap.createCommand("cmdBool", "Expect a boolean argument") \
		.expectBoolean(
			displayName="aBool",
		)

	cmdStr = ap.createCommand("cmdStr", "Expect a boolean argument") \
		.expectString(
			displayName="aStr",
		)
	cmdStr.createOption("d", "detail", "Foo Bar Help")

	cmdInt = ap.createCommand("cmdInt", "Expect an integer argument") \
		.expectInt32(
			displayName="anInt",
		)
	cmdInt.createOption("d", "detail", "Foo Bar Help")
	cmdInt.createOption("a", "anotherDetail", "Foo Bar Help")

	ap.createCommand("multiLine", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n"
		+ "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")

	# ---- parse

	ap.showHelp()

#



