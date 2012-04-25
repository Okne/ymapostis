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


'''
Created on Aug 28, 2010

@author: Denis Koronchik
'''
from distutils.core import setup


DESCRIPTION = """SC-core is a model of semantic code memory."""

METADATA = {
    "name":             "sc_core",
    "version":          "0.2.0",
    "license":          "LGPL",
    "url":              "http://www.ostis.net/",
    "author":           "Lazurkin Dmitry",
    "author_email":     "",
    "description":      "swigwin python binding for sc-core",
    "long_description": DESCRIPTION,
}

PACKAGEDATA = {
       "packages":    ['sc_core'
                        ],
                        
       "package_dir": {'': ''},
       "package_data": {'': ['*.pyd', '*.dll', '*.so', '*.dylib']}

}

if __name__ == '__main__':
    PACKAGEDATA.update(METADATA)
    setup(**PACKAGEDATA)