
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
import platform

bin = None
M4 = None
M4SCP = None
SCS2TGF = None
META = "META"
PATH_REPO_SRC = None
PATH_REPO_BIN = None
INCLUDES = None
NEW_SC_MODEL = True
NEW_STYLE_BINARY_PAIRS = True

if platform.code == platform.Windows:
    bin = "bin" + os.sep

    M4 = bin + "m4.exe"
    M4SCP = bin + "m4scp.m4"
    SCS2TGF = bin + "scs2tgf.exe"
    META = "META"

    PATH_REPO_SRC = "../fs_repo_src"
    PATH_REPO_BIN = "../fs_repo"

    INCLUDES = os.path.join(PATH_REPO_SRC, "include")

elif platform.code == platform.Posix:
    
    bin = ""
    
    M4 = "/usr/bin/m4"
    M4SCP = "m4scp.m4"
    SCS2TGF = "/usr/local/bin/scs2tgf"
    SCC = "/usr/local/bin/scc"
    META = "META"
    
    PATH_REPO_BIN = "bin"
    PATH_REPO_SRC = "sources"
    
    INCLUDES = os.path.join(PATH_REPO_SRC, "include")
