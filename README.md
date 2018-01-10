# cp2patch
A Python module to allow creation of patch files from PTC Integrity change packages.

If you are unfortunate enough to have to deal with the virus.... err, SCCM... that is PTC Integrity (God help you), this module might come in handy. Given an Integrity host and change package number, it will create a series of PATCH files in unified diff format in a user specified directory. These can then be applied to a local project, which might just happen to be under revision control using a proper system (i.e. anything but Integrity).

## Features
* Combined command line script and Python library
* File extension filters to skip members that shouldn't technically be in your Integrity project (for example, binary files)
* Patch files generated in unified diff format

## Requirements
* Windows only (could theoretically work on Linux systems, but untested)
* Python 2.7.x (Python3 support planned in future)
* PTC Integrity (currently tested with version 10.6)

## License
Free software, according to the terms of the [license agreement](LICENSE.md).

## Disclaimer
This program is still in active development, and although feature complete, testing at this point is extremely limited.

## Usage

### As a Command Line Script

```
usage: cp2patch.py [-h] [--hostname HOSTNAME] [--port PORT] --username
                   USERNAME --password PASSWORD
                   [--exclude EXCLUDE | --include INCLUDE]
                   [--destination DESTINATION]
                   cp

Create patch files from Integrity change package.

positional arguments:
  cp                    change package number

optional arguments:
  -h, --help            show this help message and exit
  --hostname HOSTNAME   Integrity host name
  --port PORT           port number
  --username USERNAME   Integrity user name
  --password PASSWORD   Integrity password
  --exclude EXCLUDE     file extensions to exclude
  --include INCLUDE     file extensions to include
  --destination DESTINATION
                        destination path for patch files
```

**Examples:**

Create patch files for change package 345 in current directory, but only for .cpp and .h files:
```
python cp2patch.py --hostname myserver.integrity.com --port 80 --username foo_bar --password she_bang --include="*.cpp *.h" 345
```

Create patch files for change package 4080 in *C:\Temp\Patch*. Exclude .out and .bin files:
```
python cp2patch.py --hostname myserver.integrity.com --port 80 --username foo_bar --password she_bang --exclude="*.out *.bin" --destination="C:\Temp\Patch" 4080
```

### As a Library

To use the library, an instance of the CP2Patch object is first created with the appropriate parameters.

\_\_init\_\_(*cpnum*, *hostname=*None, *port=*None, *username=*None, *password=*None, *exclude=*None, *include=*None, *destination=*None)

* *cpnum*: Specifies the Integrity change package number.
* *hostname*: Integrity host name to connect to.
* *username*: Integrity user name to connect with.
* *password*: Integrity password for specified user name.
* *exclude*: A string of file extensions to exclude (ex. "*.out *.bin"). Cannot be used in conjunction with *include* parameter.
* *include*: A string of file extensions to include (same format as *exclude*). Cannot be used in conjunction with *exclude* parameter.
* *destination*: Destination path for resulting patch files. Default is current directory.

**Note:** All parameters are passed as strings.

After this, the make_patch() method is called to pull the change package information from the specified server, extract the change package members and diffs, and create the patch files. One patch file is specified for each change package member.

**Example:**

```
cp2patch = CP2Patch("345", "myserver.integrity.com", port="80", username="foo_bar", password="she_bang", exclude="*.exe *.png")
cp2patch.make_patch()
```
The *destination* parameter, just as with the *--destination* argument to the command line invocation, supports both Windows and Unix style paths. Either of the following are valid:
```
cp2patch = CP2Patch("4080", "myserver.integrity.com", port="80", username="foo_bar", password="she_bang", exclude="*.exe *.png", destination="c:\Users\foo_bar\Patches")

cp2patch = CP2Patch("4080", "myserver.integrity.com", port="80", username="foo_bar", password="she_bang", exclude="*.exe *.png", destination="c:/Users/foo_bar/Patches")

```