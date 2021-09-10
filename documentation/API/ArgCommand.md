Instances of class `ArgCommand` represent a command line argument with parameters.

# Read-Only Properties

* `str name`
* `str description`

Inherited from `ArgItemBase`:

* `OptionParameter[] optionParameters`

# Read-Write Properties

* `callable onOption`

# Methods

Inherited from `ArgItemBase`:

* `ArgOption expectFileOrDirectory(str displayName, int? minLength, int? maxLength, bool mustExist = False, bool toAbsolutePath = False, str? baseDir)`
* `ArgOption expectFile(str displayName, int? minLength, int? maxLength, bool mustExist = False, bool toAbsolutePath = False, str? baseDir)`
* `ArgOption expectDirectory(str displayName, int? minLength, int? maxLength, bool mustExist = False, bool toAbsolutePath = False, str? baseDir)`
* `ArgOption expectString(str displayName, int? minLength, int? maxLength, str[] enumValues = None, str? regex)`
* `ArgOption expectInt32(str displayName, int? minValue, int? maxValue)`

















