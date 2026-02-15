Instances of class `ArgOption` represent an option that can be specified on the command line.

# Read-Only Properties

* `str? shortName`
* `str? longName`
* `str description`
* `bool isRequired`
* `bool isShortOption`

Inherited from `ArgItemBase`:

* `OptionParameter[] optionParameters`

# Read-Write Properties

* `callable onOption`

# Methods

* `ArgOption required(str errorMessage)`

Inherited from `ArgItemBase`:

* `ArgOption expectFileOrDirectory(str displayName, int? minLength, int? maxLength, bool mustExist = False, bool toAbsolutePath = False, str? baseDir)`
* `ArgOption expectFile(str displayName, int? minLength, int? maxLength, bool mustExist = False, bool toAbsolutePath = False, str? baseDir)`
* `ArgOption expectDirectory(str displayName, int? minLength, int? maxLength, bool mustExist = False, bool toAbsolutePath = False, str? baseDir)`
* `ArgOption expectString(str displayName, int? minLength, int? maxLength, str[] enumValues = None, str? regex)`
* `ArgOption expectInt32(str displayName, int? minValue, int? maxValue)`

















