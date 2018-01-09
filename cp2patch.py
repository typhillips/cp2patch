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

		# Create list of "standard" si arguments that will be used on all Integrity commands
		self.std_args = []

		if self.hostname:
			self.std_args.append("--hostname=" + self.hostname)
		if self.port:
			self.std_args.append("--port=" + self.port)

		self.std_args.append("--user=" + self.username)
		self.std_args.append("--password=" + self.password)

	def make_patch(self):
		"""Create patch files."""

		# First get change package information
		cpinfo = self.get_cpinfo()

		# Iterate through each member of change package
		for item in cpinfo:
			member = item[0]
			project = item[1]
			rev = item[2]

			#---- Determine previous member revision for each member
			si_args = ["si"]
			si_args.append("rlog")
			si_args.append("--project=" + project)
			si_args += self.std_args
			si_args.append("--fields=revision")
			si_args.append(member)

			# This gives us a list of lines of the 'rlog' output
			cmd_out = subprocess.check_output(si_args).split("\n")

			# Get list index with revision number we are interested in and find the next entry
			#   This is previous revision
			prev_rev = cmd_out[cmd_out.index(rev) + 1]

			#---- Get member files for old and new revisions
			si_args = ["si"]
			si_args.append("viewrevision")
			si_args.append("-r")
			si_args.append(prev_rev)
			si_args.append("--project=" + project)
			si_args += self.std_args
			si_args.append(member)

			# List of lines of old file
			old_file = subprocess.check_output(si_args).splitlines(True)

			si_args = ["si"]
			si_args.append("viewrevision")
			si_args.append("-r")
			si_args.append(rev)
			si_args.append("--project=" + project)
			si_args += self.std_args
			si_args.append(member)

			# List of lines of new file
			new_file = subprocess.check_output(si_args).splitlines(True)

			# Get member relative path
			#   Strip off everything up to and include development path name
			#   For example:
			#     "#/Project/#d=Subproject/Foo/Bar" --> "Foo/Bar"
			#     "#/Project/#d=Subproject#Foo/Bar" --> "Foo/Bar"
			member_path = ""
			m = re.split("#d=[^#/]+[#/]", project)

			if len(m) > 1:
				member_path += m[1] + "/"

			# Strip out any remaining "well formed project name" hash characters
			member_path.replace("#/", "/")
			member_path.replace("#", "/")

			# Add member file name to end of path
			member_path += member

			#debug-----------------------------------
			patch_lines = difflib.unified_diff(old_file, new_file, fromfile=member_path, tofile=member_path)
			for line in patch_lines:
				sys.stdout.write(line)
			#end debug-------------------------------

	def get_cpinfo(self):
		""" Returns a list with each change package member, its associated project and its revision."""
		si_args = ["si"]
		si_args.append("viewcp")
		si_args += self.std_args
		si_args.append("--fields=member,configpath,revision")
		si_args.append("--noshowPropagationInfo")
		si_args.append(self.cpnum)

		# This gives us a list of lines of the 'viewcp' output
		cmd_out = subprocess.check_output(si_args).split("\n")

		# Strip off first line with change package number and project - we don't need this
		cmd_out = cmd_out[1:]

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

		for line in cmd_out:
			data = line.split()		# Get list of member, project, revision

			if len(data) == 3:		# Ignore any blank lines
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
		self.exclude = args.exclude
		self.include = args.include
		self.destination = args.destination
		self.cpnum = args.cp

	def run(self):
		cp2patch = CP2Patch(self.cpnum, hostname=self.hostname, port=self.port, username=self.username, password=self.password, \
		                    exclude=self.exclude, include=self.include, destination=self.destination)
		cp2patch.make_patch()


if __name__ == "__main__":
	app = ShellRun()
	app.run()