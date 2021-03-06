# cp2patch
A Python module to allow creation of patch files from PTC Integrity change packages.

If you are unfortunate enough to have to deal with the virus.... err, SCCM... that is PTC Integrity (God help you), this module might come in handy. Given an Integrity host and change package number, it will create a series of PATCH files in unified diff format in a user specified directory. These can then be applied to a local project, which might just happen to be under revision control using a proper system (i.e. anything but Integrity).

## Features
* Combined command line script and Python library
* File extension and string matching filters to skip members that cannot be patched
* Patch files generated in unified diff format
* Binary file capability

## Requirements
* Python 2.7 / 3.6
* PTC Integrity (currently tested with version 10.6)
* [bsdiff4](https://pypi.org/project/bsdiff4/) module (for binary patch)

## Limitations
* Windows only (could theoretically work on Linux systems, but untested)
* Might not work correctly for Integrity revision numbers that are manually assigned during check in - this is due to the fact that the previous revision number of a given member revision must be derived manually since the Integrity CLI cannot report it

## License
Free software, according to the terms of the [license agreement](LICENSE.md).

## Disclaimer
This program is still in active development, and although feature complete, testing at this point is extremely limited.

## Usage

### As a Command Line Script

#### For text files:
```
usage: cp2patch.py [-h] [--hostname HOSTNAME] [--port PORT] --username
                   USERNAME --password PASSWORD
                   [--exclude EXCLUDE | --include INCLUDE]
                   [--destination DESTINATION] [--encoding ENCODING]
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
  --nomatch NOMATCH     member filenames containing this string will be
                        excluded
  --match MATCH         member filenames containing this string will be
                        included
  --destination DESTINATION
                        destination path for patch files
  --encoding ENCODING   set character encoding used for Integrity CLI output

```
#### For binary files:
```
usage: cp2patch-bin.py [-h] [--hostname HOSTNAME] [--port PORT] --username
                       USERNAME --password PASSWORD
                       [--exclude EXCLUDE | --include INCLUDE]
                       [--destination DESTINATION] [--encoding ENCODING]
                       cp

Create binary patch files from Integrity change package.

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
  --nomatch NOMATCH     member filenames containing this string will be
                        excluded
  --match MATCH         member filenames containing this string will be
                        included
  --destination DESTINATION
                        destination path for patch files
  --encoding ENCODING   set character encoding used for Integrity CLI output
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

Create patch files for change package 229:3. Exclude .srec files. Use Arabic encoding:
```
python cp2patch.py --hostname myserver.integrity.com --port 80 --username foo_bar --password she_bang --exclude="*.srec" --encoding="iso8859_6" 229:3
```

Create patch files for change package 1028:2. Include only *.h files containing the string "definition":
```
python cp2patch.py --hostname myserver.integrity.com --port 80 --username foo_bar --password she_bang --include="*.h" --match="definition" 1028:2
```

Create binary patches for all *.bin files in change package 1028:2:
```
python cp2patch-bin.py --hostname myserver.integrity.com --port 80 --username foo_bar --password she_bang --include="*.bin" 1028:2
```

### As a Library

To use the library, an instance of the CP2Patch or CP2PatchBin (for binary files) object is first created with the appropriate parameters.

\_\_init\_\_(*cpnum*, hostname=None, port=None, username=None, password=None, exclude=None, include=None, destination=None)

* *cpnum*: Specifies the Integrity change package number.
* *hostname*: Integrity host name to connect to.
* *username*: Integrity user name to connect with.
* *password*: Integrity password for specified user name.
* *exclude*: A string of file extensions to exclude (ex. "*.out *.bin"). Cannot be used in conjunction with *include* parameter.
* *include*: A string of file extensions to include (same format as *exclude*). Cannot be used in conjunction with *exclude* parameter.
* *nomatch*: Members with filenames containing this string will be excluded. Cannot be used in conjunction with *match* parameter.
* *match*: Only members with filenames containing this string will be included. Cannot be used in conjunction with *nomatch* parameter.
* *destination*: Destination path for resulting patch files. Default is current directory.
* *encoding*: Set character encoding for Integrity CLI output. Default is ASCII.

**Note:** All parameters are passed as strings.

After this, the make_patch() method is called to pull the change package information from the specified server, extract the change package members and diffs, and create the patch files. One patch file is specified for each change package member.

**Example:**

```
cp2patch = CP2Patch("345", hostname="myserver.integrity.com", port="80", username="foo_bar", password="she_bang", exclude="*.exe *.png")
cp2patch.make_patch()
```
The *destination* parameter, just as with the *--destination* argument to the command line invocation, supports both Windows and Unix style paths. Either of the following are valid:
```
cp2patch = CP2Patch("4080:1", hostname="myserver.integrity.com", port="80", username="foo_bar", password="she_bang", exclude="*.exe *.png", destination="c:\Users\foo_bar\Patches")

cp2patch = CP2Patch("4080:1", hostname="myserver.integrity.com", port="80", username="foo_bar", password="she_bang", exclude="*.exe *.png", destination="c:/Users/foo_bar/Patches")

```
