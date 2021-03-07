Instances of class `ArgsParser` define the data model of the arguments to parse.
Such instances will have a variety of properties and methods that are described below.

# Properties

* `ArgsOptionDataDict optionDataDefaults`
* `str appName`
* `str shortAppDescription`

# Methods

* `ArgCommand createCommand(name, description)`
* `ArgOption createOption(str? shortName, str? longName, str description)`
* `void showHelp()`
* `ArgsParser createSynopsis(str synopsis)`
* `ArgsParser createAuthor(str name, str email = None)`
* `ArgsParser createReturnCode(int returnCode, str description)`
* `ArgsParser setLicense(licenseID:str, **kwargs)`
* `ArgsParser addDescriptionChapter(chapterName:str, paragraphs:list)`
* `str[] buildHelpText()`
* `ParsedArgs parse(args = None)`
* `str createBashCompletionFileText()`


















