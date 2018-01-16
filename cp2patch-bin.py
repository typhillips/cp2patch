# cp2patch
#
# Copyright 2018 Ty Phillips. All Rights Reserved.
# This program is free software. You can redistribute and/or modify it in
# accordance with the terms of the accompanying license agreement.

#!/usr/bin/env python

import os
import argparse
import subprocess
import cp2patch
import bsdiff4

class CP2PatchBin(cp2patch.CP2Patch):

	def make_patch(self):
		"""Create patch files."""

		# First get change package information
		cpinfo = self.get_cpinfo()
		# Iterate through each member of change package
		for item in cpinfo:
			member = item[0]
			project = item[1]
			rev = item[2]

			# Get previous member revision
			prev_rev = self.get_prev_rev(member, project, rev)

			#---- Get member files for old and new revisions
			si_args = ["si"]
			si_args.append("viewrevision")
			si_args.append("-r")
			si_args.append(prev_rev)
			si_args.append("--project=" + project)
			si_args += self.std_args
			si_args.append(member)

			# String representing old file
			old_file_st = subprocess.check_output(si_args)

			si_args = ["si"]
			si_args.append("viewrevision")
			si_args.append("-r")
			si_args.append(rev)
			si_args.append("--project=" + project)
			si_args += self.std_args
			si_args.append(member)

			# String representing new file
			new_file_st = subprocess.check_output(si_args)

			# Open file for writing
			#   Binary patch file naming convention: "foobar.out" becomes "foobar_out.bsdiff"
			filename = os.path.splitext(member)[0] + "_" + os.path.splitext(member)[1].lstrip(".") + ".bsdiff"

			# Prepend destination path if specified
			if self.destination:
				dir_normalized = os.path.normpath(self.destination)	# Get normalized path Python can understand

				# If invalid path specified, patch files go in current directory
				if os.path.isdir(dir_normalized):
					filename = os.path.join(os.path.normpath(self.destination), filename)

			outfile = open(filename, 'wb')

			# Create patch
			patch = bsdiff4.diff(old_file_st, new_file_st)

			# Write lines of patch output to file
			outfile.write(patch)

			outfile.close()


class ShellRun(object):
	def __init__(self):
		parser = argparse.ArgumentParser(description="Create binary patch files from Integrity change package.")
		parser.add_argument("--hostname", help="Integrity host name")
		parser.add_argument("--port", help="port number")
		parser.add_argument("--username", help="Integrity user name", required=True)
		parser.add_argument("--password", help="Integrity password", required=True)

		# --include / --exclude  cannot both be used at the same time
		group = parser.add_mutually_exclusive_group()
		group.add_argument("--exclude", help="file extensions to exclude")
		group.add_argument("--include", help="file extensions to include")

		parser.add_argument("--destination", help="destination path for patch files")
		parser.add_argument("cp", help="change package number")
		args = parser.parse_args()

		self.hostname = args.hostname
		self.port = args.port
		self.username = args.username
		self.password = args.password
		self.exclude = args.exclude
		self.include = args.include
		self.destination = args.destination
		self.cpnum = args.cp

	def run(self):
		cp2patch = CP2PatchBin(self.cpnum, hostname=self.hostname, port=self.port, username=self.username, password=self.password, \
		                    exclude=self.exclude, include=self.include, destination=self.destination)
		cp2patch.make_patch()


if __name__ == "__main__":
	app = ShellRun()
	app.run()