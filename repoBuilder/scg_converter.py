
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



import myutil
import os
import scg2scs
import sys
import defines
from converter import Converter
from subprocess import Popen, PIPE
import platform

class ScgConverter(Converter):

    def type(self, filePath):
        return myutil.fileType(filePath, "scg")

    def runConvertation(self, pathSrc, pathBin):
        myutil.createDirs(pathBin)
        pathSrcDir = os.path.dirname(pathSrc)

        scg2scs.parse_scg(pathSrc)
        tmpfile = os.tmpfile() #open(pathSrc + ".tscs", "w")
        scg2scs.write_scs(tmpfile)
        
        #print tmpfile.name
        

#   dfile = open(pathBin + ".tscs", "w")
#   scg2scs.write_scs(dfile)
#   dfile.close()

        tmpfile.seek(os.SEEK_SET)

        #cmd = [defines.SCS2TGF, '-nc', '-I' + defines.INCLUDES, '-I' + os.path.dirname(pathSrc), '-', pathBin]
        
        if defines.NEW_SC_MODEL:
            cmd = [defines.SCC, '-', '-a', '-I %s' % (defines.INCLUDES), '-I %s' % (os.path.dirname(pathSrc)), '-o %s' % (pathBin)]
            process = Popen(cmd, stdin=tmpfile, stdout=PIPE, stderr=PIPE)
        else:
            cmd = ['-nc', '-I%s' % defines.INCLUDES, '-I%s' % os.path.dirname(pathSrc), '-', pathBin]
            process = Popen(cmd, executable=defines.SCS2TGF, stdin=tmpfile, stdout=PIPE, stderr=PIPE)
        process.wait()

        try:
            if process.returncode == 0:
                return True
            else:
                print >> sys.stderr, "In file %s:" % (pathSrc)
                myutil.printPipe(sys.stderr, process.stderr)
                return False
        finally:
            process.stdout.close()
            process.stderr.close()

