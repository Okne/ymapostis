#! /usr/bin/env python
"""
-----------------------------------------------------------------------------
This source file is part of OSTIS (Open Semantic Technology for Intelligent Systems)
For the latest info, see http://www.ostis.net

Copyright (c) 2010 OSTIS

OSTIS is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OSTIS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with OSTIS.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
"""

import os
import os.path
from subprocess import Popen
from subprocess import PIPE
import sys

import myutil
from defines import *
from m4scp_converter import M4ScpConverter
from scs_converter import ScsConverter
from scg_converter import ScgConverter
from converter import SkipConverter

class Builder:
	"""General class
	Class contein all objects of converters
	Class parse all files and run current converter
	"""
	def __init__(self):
		self.converters = [ScsConverter(), M4ScpConverter(), ScgConverter()]#, SkipConverter()]
		self.errors = 0

	def run(self):
		myutil.cleanDir(PATH_REPO_BIN)	
		self.scan(PATH_REPO_SRC)
		os.mkdir(PATH_REPO_BIN + "/tmp")
		os.mkdir(PATH_REPO_BIN + "/proc")
		self.createMetaFiles(PATH_REPO_BIN)
		sys.stderr.flush()
		print "Find", self.errors, "errors"
		
	def scan(self, path):
		"""find current files and run converters"""
		if os.path.isfile(path):
			converter = self.defineConverter(path)
			if not converter is None:
				print "build " + path
				if not converter.convert(path):
					self.errors = self.errors + 1
			#else:
			#	print >> sys.stderr, "Not handled", path
		elif os.path.isdir(path) and path != INCLUDES and (os.path.basename(path).startswith(".") is False):
			listDirs = os.listdir(path)
			for i in listDirs:
				self.scan(path + "/" + i)

	def defineConverter(self, filePath):
		"""Return instance of converter"""
		for c in self.converters:
			if c.type(filePath):
				return c

	def createMetaFiles(self, dir):
		"""Create META File in directory"""
		listDirs = os.listdir(dir)
		metaStr = self.collectMeta(listDirs)
		pathBin = dir + "/" + META
		print "Generate %s/META" % dir
		cmdScs = "%s -nc - %s" % (SCS2TGF, pathBin)
		process = Popen(cmdScs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		process.stdin.write(metaStr)
		process.stdin.close()
		process.wait()
		for i in listDirs:
			path = dir + "/" + i
			if os.path.isdir(path):
				self.createMetaFiles(path)

	def collectMeta(self, listDirs):
		"""Return str of META"""
		if META not in listDirs:
			listDirs.insert(0, META)
		else:
			myutil.showWarning("META file is exists and has been rewrited")
		meta = ""
		meta = meta + ('\"/info/derent\" = {\n')
		meta = meta + ('\t"' + listDirs[0] + '\"={}')
		for i in listDirs[1:]:
			meta = meta + (',\n\t\"' + i + '\"={}')
		meta = meta +('\n};\n')
		return meta


if __name__ == "__main__":
	builder = Builder()
	builder.run()
