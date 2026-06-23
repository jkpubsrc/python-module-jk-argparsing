

import jk_logging
import jk_assert

import jk_argparsing





with jk_logging.wrapMain() as log:

	# ---- definition

	ap = jk_argparsing.ArgsParser("foobar", "Lorem ipsum dolor sid amet")

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

	ap.createCommand("cmdBool", "Expect a boolean argument") \
		.expectBoolean(
			displayName="aBool",
		)
	ap.createCommand("cmdStr", "Expect a boolean argument") \
		.expectString(
			displayName="aStr",
		)
	ap.createCommand("cmdInt", "Expect an integer argument") \
		.expectInt32(
			displayName="anInt",
		)

	# ---- parse

	parsedArgs = ap.parse([
		"--parse-strlist", "foo,bar,baz",
		"--parse-bool", "yes",
		"--parse-int", "2345",
		"cmdBool", "1",
		"cmdStr", "Some string",
		"whatever", "12345",
	])

	parsedArgs.dump()

	# ---- verify options

	jk_assert.assertEquals(parsedArgs.optionData, {
		"aStrListValue": [ "foo", "bar", "baz" ],
		"anInt": 2345,
		"aBool": True,
	})

	# ---- verfiy commands

	jk_assert.assertEquals(parsedArgs.terminate, False)
	jk_assert.assertEquals(parsedArgs.programArgs, [
		"cmdBool", "1",
		"cmdStr", "Some string",
		"whatever", "12345",
	])

	print()
	commands = list(parsedArgs.parseCommands())

	raise Exception("We should not arrive in this line here!")

#



