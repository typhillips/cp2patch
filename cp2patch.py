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
import re

class CP2Patch(object):
	def __init__(self, cpnum, hostname=None, port=None, username=None, password=None, exclude=None, include=None, destination=None):
		self.hostname = hostname
		self.port = port
		self.username = username
		self.password = password
		self.exclude = exclude
		self.include = include
		self.destination = destination
		self.cpnum = cpnum

	def make_patch(self):
		"""Create patch files."""

		# First get change package information (list of members and their versions)
		cpinfo = self.get_cpinfo()
		print cpinfo #debug

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
		""" Returns a list with change package members and their revisions."""
		si_args = ["si"]
		si_args.append("viewcp")

		if self.hostname:
			si_args.append("--hostname=" + self.hostname)
		if self.port:
			si_args.append("--port=" + self.port)

		si_args.append("--user=" + self.username)
		si_args.append("--password=" + self.password)
		si_args.append("--fields=member,configpath,revision")
		si_args.append("--noshowPropagationInfo")
		si_args.append(self.cpnum)

		# This gives us a list of lines of the 'viewcp' output
		viewcp_out = subprocess.check_output(si_args).split("\n")

		# Strip off first line with change package number and project - we don't need this
		viewcp_out = viewcp_out[1:]

		cpinfo = []
		exts_exclude = []
		exts_include = []

		# Get file extensions to include or exclude
		if self.exclude:
			exts_exclude = self.get_extension_list(self.exclude)
		elif self.include:
			exts_include = self.get_extension_list(self.include)
		else:
			pass

		for line in viewcp_out:
			data = line.split()		# Get list of member, project, revision

			if len(data) == 3:		# Ignore any blank lines
				del data[1]			# Remove project field - list now contains member, revision

				# File extension filters
				file_ext = os.path.splitext(data[0])[1].lower()			# Get member's file extension

				# No filters specified OR inclusion filter match OR exclusion filter no match
				if ( not (exts_include or exts_exclude) or \
				     (exts_include and (file_ext in exts_include)) or \
				     (exts_exclude and (file_ext not in exts_exclude))
				   ):
					cpinfo.append(data)

		return cpinfo

	def get_extension_list(self, exts):
		"""Given a string of file extensions, extract these and return a list of file extensions.
		   Invalid entries are ignored."""
		exts_list = []

		# Check that each file extension is specified as "*.ext" using regex
		for item in exts.split():
			m = re.match('[*][.].+', item)

			if m:
				exts_list.append(m.group().lstrip('*').lower())	# Extension string as ".ext" (lowercase)

		return exts_list


class ShellRun(object):
	def __init__(self):
		parser = argparse.ArgumentParser(description="Create patch files from Integrity change package.")
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
		self.include = args.include
		self.exclude = args.exclude
		self.destination = args.destination
		self.cpnum = args.cp

	def run(self):
		cp2patch = CP2Patch(self.cpnum, hostname=self.hostname, port=self.port, username=self.username, password=self.password, \
		                    exclude=self.exclude, include=self.include, destination=self.destination)
		cp2patch.make_patch()


if __name__ == "__main__":
	app = ShellRun()
	app.run()