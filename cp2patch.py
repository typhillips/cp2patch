
# cp2patch
#
# Copyright 2017 Ty Phillips. All Rights Reserved.
# This program is free software. You can redistribute and/or modify it in
# accordance with the terms of the accompanying license agreement.

#!/usr/bin/env python

import sys
import os
import difflib
import argparse
import subprocess

class CP2Patch(object):
	def __init__(self, cpnum, hostname=None, username=None, password=None, destination=None):
		self.hostname = hostname
		self.username = username
		self.password = password
		self.destination = destination
		self.cpnum = cpnum

	def make_patch(self):
		cpinfo = self.get_cpinfo()

		for filename in cpinfo:
			#TODO
			# Run 'si viewrevision' to dump old and new revisions to
			#   new files
			# Use difflib.unified_diff() to generate patch files
			# Somehow come up with a way to generate an error (and/or skip patch file creation) if patch fails
			#
			# patch_lines = difflib.unified_diff(file1.readlines(), file2.readlines(), fromfile=os.path.abspath("file1"), tofile=os.path.abspath("file2"))

			# for line in patch_lines:
			#	sys.stdout.write(line)
			pass



	def get_cpinfo(self):
		#TODO
		# Run 'si viewcp' to get list of files and version numbers
		# For each file
		#   Run 'si rlog' on each file
		#   Search output to find version number and previous version number
		#   Add this to the running list
		# Return list of files with new and old version numbers
		si_args = ["si"]
		si_args.append("viewcp")
		si_args.append("hostname=" + self.hostname)
		si_args.append("user=" + self.username)
		si_args.append("password=" + self.password)
		si_args.append(str("cp"))

		cpinfo = subprocess.check_output(si_args).split("\n")

		for line in cpinfo:
			#TODO Iterate through CP info and convert to list of files and versions
			pass
		return []



class ShellRun(object):
	def __init__(self):
		parser = argparse.ArgumentParser(description="Create PATCH files from Integrity change package.")
		parser.add_argument("-n", "--hostname", help="Integrity host name")
		parser.add_argument("-u", "--username", help="Integrity user name")
		parser.add_argument("-p", "--password", help="Integrity password")
		parser.add_argument("-d", "--destination", help="destination path for files")
		parser.add_argument("cp", type=int, help="change package number")
		args = parser.parse_args()

		self.hostname = args.hostname
		self.username = args.username
		self.password = args.password
		self.destination = args.destination
		self.cpnum = args.cp

	def run(self):
		cp2patch = CP2Patch(self.cpnum, hostname=self.hostname, password=self.password, destination=self.destination)
		cp2patch.make_patch()


if __name__ == "__main__":
	app = ShellRun()
	app.run()
