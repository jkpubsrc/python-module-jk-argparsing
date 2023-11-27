#!/usr/bin/python3


import jk_logging
import jk_testing

import jk_argparsing




with jk_logging.wrapMain() as log:

	ap = jk_argparsing.ArgsParser("foobar", "Lorem ipsum dolor sid amet")

	ap.createOption("h", "help", "Display a help page")
	ap.createOption(None, "parse-strlist", "Parse a string list") \
		.expectCommaSeparatedStringList(
			displayName="aStrList",
			listMinLength=1,
			strMinLength=3,
		).onOption = lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("aStrListValue", argOptionArguments[0])

	parsedArgs = ap.parse([
		"--parse-strlist", "foo,bar,baz", "extraFoo", "extraBar"
	])

	parsedArgs.dump()

	jk_testing.Assert.isEqual(parsedArgs.optionData, {
		"aStrListValue": [ "foo", "bar", "baz" ],
	})
	jk_testing.Assert.isEqual(parsedArgs.terminate, False)
	jk_testing.Assert.isEqual(parsedArgs.programArgs, [ "extraFoo", "extraBar" ])




