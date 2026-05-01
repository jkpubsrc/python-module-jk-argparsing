

import jk_logging

import jk_argparsing
import jk_argparsing.textmodel




LOREM_IPSUM_SHORT = "Lorem ipsum dolor sid amet."
LOREM_IPSUM_MULTILINE = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n" \
	"At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
LOREM_IPSUM_LONG = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. " \
	"At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
GALLIA = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur."
THE_QUICK_BROWN_FOX = "The quick brown fox jumps over the lazy dog."




with jk_logging.wrapMain() as log:

	# ---- definition

	ap = jk_argparsing.ArgsParser("foobar", LOREM_IPSUM_SHORT)

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

	ap.createCommand("multiLine", LOREM_IPSUM_MULTILINE)

	# ----

	ap.createSynopsis(LOREM_IPSUM_LONG)
	ap.createSynopsis(THE_QUICK_BROWN_FOX)

	ap.createAuthor("Foo Bar", "foo@bar.com", "Some author")
	ap.createAuthor("Tabea Tester", "tabea@tester.com")

	ap.createReturnCode(0, "Success")
	ap.createReturnCode(1, "Some error")
	ap.createReturnCode(1, "Another error")

	ap.createEnvVar("FOO_BAR", LOREM_IPSUM_SHORT)

	ap.setLicense("Apache2")

	# ----

	ap.addDescriptionChapter(None, [
		LOREM_IPSUM_SHORT,
	])
	ap.addDescriptionChapter("Foo", [
		GALLIA,
	])
	ap.addDescriptionChapter(None, [
		THE_QUICK_BROWN_FOX,
	])

	# ----

	ap.addExtraChapterHead(
		jk_argparsing.textmodel.TSection("Extra_Chapter_Head", [ LOREM_IPSUM_LONG ])
	)

	ap.addExtraChapterMiddle(
		jk_argparsing.textmodel.TSection("Extra_Chapter_Middle", [ LOREM_IPSUM_LONG ])
	)

	ap.addExtraChapterEnd(
		jk_argparsing.textmodel.TSection("Extra_Chapter_End", [ LOREM_IPSUM_LONG ])
	)

	# ---- display help text

	ap.showHelp()

#



