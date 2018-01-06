# cp2patch #
A Python module to allow creation of patch files PTC Integrity change packages.

If you are unfortunate enough to have to deal with the virus.... err, SCCM... that is PTC Integrity (God help you), this module might come in handy. Given an Integrity host and change package number, it will create a series of PATCH files in unified diff format in a user specified directory. These can then be applied to a local project, which might just happen to be under revision control using a proper system (i.e. anything but Integrity).

## Requirements ##
* Windows only
* Python 2.7.x
* PTC Integrity

More information TBD.
