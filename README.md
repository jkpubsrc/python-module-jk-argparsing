﻿jk_argparsing
=============

Introduction
------------

This module provides an API for processing command line arguments. There is ``argparse`` of course, but this API is better. Better means: Simpler, more easy to use.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-argparsing)
* [pypi.python.org](https://pypi.python.org/pypi/jk_argparsing)

History
----------------------

Not every piece of software has a history. This module has.

Work on this module began over a decade ago in a complete different programming language: C#. As I required some command line tools in C# I implemented a .Net library for that purpose as there was nothing like that I could use. This library was so convenient that a) I prepared it for release under the Apache Open Source license and b) ported it to Python some years later.

So this python module here is based on that .Net library. It is basically a port of that library. However, year after year I improved that Python module bit by bit, so this Python module became a very convenient tool, way beyond the original capabilities of that .Net library.

The next sections provide detailed information about how to use `jk_argparsing`.

How to use this module
----------------------

## Import

To import this module use the following statement:

```python
import jk_argparsing
```

## Concept

First some short information about terminology used by this module:

* An *option* is something like `-h` or `-l` or `--help`. (e.g.: `ls -la`)
* A *command* is something like `update` or `install` or whatever. (e.g.: `apt update`)

NOTE: Command line parsing will follow these conceps (and only these concepts) listed above.

Using `jk_argparsing` is very simple:

* You first instantiate an object of `ArgsParser`.
* Then you define defaults in a data dictionary for your options.
* Then you configure this object by invoking methods on this object. By doing this you define ...
	* the author(s) of your program
	* the license your program will be using
	* options, your program might require (together with expectations for arguments to provide)
	* commands, your program might provide (together with expectations for arguments to provide)
	* exit codes, your program might use
	* various other information useful for a user
* After configuration is complete, you invoke `parse()` to initiate parsing of the command line specified by the user. In doing so ...
	* program options are parsed and entries in your data dictionary will be modified in the process.
	* An object of type `ParsedArgs` will now be returned.
* You can now use this returnes object to process the commands provided on the command line.

## Example

First, let's create an instance of `ArgsParser`:

```python
ap = ArgsParser(appName="myapp", shortAppDescription="My short description")
```

Then let's configure this object. The following is just an example of what you might want to do:

```python
ap.createSynopsis("myapp -x foo")
ap.createSynopsis("myapp -y bar")

ap.optionDataDefaults.set("help", False)

ap.createOption(None, "enabled", "Something is enabled.").expectString("OPT1", minLength = 2).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("my", argOptionArguments[0])
ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
ap.createOption("n", "nothing", LOREM_IPSUM)

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("apache", YEAR = 2017, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An I/O error occurred.")
ap.createReturnCode(-1, "Invalid configuration.")

ap.createCommand("foo", "Lorem ipsum dolor sid amet.")
ap.createCommand("bar", "The quick brown fox jumps over the lazy dog.")
```

Now if you would generate a help text by invoking `ap.showHelp()` you would get this result:

```
myapp - My short description

SYNOPSIS

    myapp -x foo
    myapp -y bar

OPTIONS

        --enabled OPT1  Something is enabled.
    -h  --help          Display this help text.
    -n  --nothing       Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse congue, orci vel interdum bibendum, nisi mauris
                        porttitor tortor, non tincidunt neque quam eget est. Vivamus sollicitudin urna ut elit lobortis, eget pretium est
                        sollicitudin. Vivamus venenatis ut erat quis gravida. Praesent vel purus finibus velit pretium eleifend.

COMMANDS

    bar  The quick brown fox jumps over the lazy dog.
    foo  Lorem ipsum dolor sid amet.

PROGRAM EXIT CODES

    0   Everything is okay.
    1   An I/O error occurred.
    -1  Invalid configuration.

AUTHORS

    Jürgen Knauth <jk@binary-overflow.de>

LICENSE

    This program is free software: you can redistribute it and/or modify it under the terms of the Apache Software License as published by
    Apache Software Foundation in version 2. For more details see the Apache Software License, which should be vailable at:
    https://www.apache.org/licenses/LICENSE-2.0
```

## Adding a description

You might want to add a description. For better readability this description could have chapters:

```python
ap.addDescriptionChapter("Introduction", "Lorem ipsum dolor sid amet ...")
ap.addDescriptionChapter("Usage", "Lorem ipsum dolor sid amet ...")
ap.addDescriptionChapter("Whatever", "Lorem ipsum dolor sid amet ...")
```

A description is placed **after** the synopsis and **before** the options.

Additional methods are provided to insert text at some other position in the help text `jk_argparsing` will create for yoou:

* `addExtraChapterHead(..)`
* `addExtraChapterMiddle(..)`
* `addExtraChapterEnd(..)`

The full help text created will then have the following structure:

| Position						| Description
| ---							| ---
| A title						| In this example here: "`myapp - My short description`"
| Synposis						| Multiple lines defined by `createSynopsis(..)`
| A head text section			| Defined by `addExtraChapterHead(..)`
| The standard description		| Defined by `addDescriptionChapter(..)`
| A middle text section			| Defined by `addExtraChapterMiddle(..)`
| Options						| A formatted table with all options provided by `createOption(..)`
| Commands						| A formatted table with all commands provided by `createCommand(..)`
| Program exit codes			| A formatted table with all exit codes provided by `createReturnCode(..)`
| A final text section			| Defined by `addExtraChapterEnd(..)`
| Authors						| A list of all authors defined by `createAuthor(..)`
| License						| A short license information defined by `setLicense(..)`

## Program options

For your program to support options your first step should be to provide default value(s) that can get modified later during parsing. Here we use `help` for demonstration purposes:

```python
ap.optionDataDefaults.set("help", False)
```

Then define the option so that the parser later will be able to process it:

```python
ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
```

In this particular case the option will have no argument.
However, the option will have a lambda function that can be assigned to `onOption`. This lambda function will be executed if the parser encounteres this option.

The lambda function will receive three arguments:
* `argOption` - The option that is currently being parsed. (You typically have no use for this parameter as by attaching a lambda function you already know the option that is going to be parsed.)
* `argOptionArguments` - A list of arguments the option might have. (This list is empty in our case as `--help` does not have any additional arguments.)
* `parsedArgs` - The `ParsedArgs` object the parser is creating by parsing the command line on `ap.parse()`. (This `ParsedArgs` object will be returned later to the caller of `ap.parse()`.)

Within this lambda functions you should access `parsedArgs.optionData`. This is a dictionary you can modify. For simplicity invoke `set(..)` to modify a values.
In this example here the original value for `help` will be overwritten.

## Program commands

For your program to support commands you just define your command. Example:

```python
ap.createCommand("update", "Perform some kind of update.")
```

Of course you could have a command with an argument:

```python
ap.createCommand("process-file", "Load a settings file.") \
	.expectFile("<settingsFile>", minLength=1, mustExist=True, toAbsolutePath=True)
```

Now if the user runs your program with arguments such as these ...

> `yourprogram process-file some/path/to/a/file`

... the parsing engine will check that a file path follows `process-file` that refers to an existing file. In addition this argument will converted to an absolute path automatically during parsing.

Processing such kind of program arguments in your program is simple. Here is an example:

```python
# parse the command line using our predefined object `ArgsParser` in `ap`
# NOTE: all options get processed automatically during this parsing step
parsedArgs = ap.parse()

if parsedArgs.optionData["help"]:
	# `help` is true, so let's exit here
	ap.showHelp()
	sys.exit(1)

if not parsedArgs.programArgs:
	# no program arguments specified, so let's exit here
	ap.showHelp()
	sys.exit(1)

for cmdName, cmdArgs in parsedArgs.parseCommands():
	if cmdName == 'update':
		# do somethig
		...
	elif cmdName == 'process-file':
		# do somethig
		...
	else:
		# fallback if - by accident - we have an error in our implementation here
		raise Exception("Implementation error!")
```

## Expectations for options and commands

Options and commands can have "expections". An expectation is an argument a user must append to the option. Example:

> `yourprogram --output-file some/path/to/a/file do-something`

Or:

> `yourprogram process-file some/path/to/a/file`

Here ...
* `--output-file` would be an option that expects one argument,
* `do-something` would be a command that has no arguments and
* `process-file` would be a command that expects one argument.

Here is how you could define such a command:

```python
ap.createCommand("process-file", "Load a settings file.") \
	.expectFile("<settingsFile>", minLength=1, mustExist=True, toAbsolutePath=True)
```

The following expectations for arguments to options and commands are available:

| Method to invoke				| Description											|
| ---							| ---													|
| `expectFileOrDirectory(..)`	| Provided argument must be a file or directory			|
| `expectFile(..)`				| Provided argument must be a file						|
| `expectDirectory(..)`			| Provided argument must be a directory					|
| `expectString(..)`			| Provided argument must be a text string				|
| `expectInt32(..)`				| Provided argument must be an integer number			|

NOTE: By definition `expectString(..)`, `expectFileOrDirectory(..)`, `expectFile(..)` and `expectDirectory(..)` are quite similar: They all specify that a string is expected. However, each method will support constraints. While `expectString(..)` only supports standard string constraints, the other methods will assume that the specified string denotes a file or directory.

Author(s)
-------------------

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



