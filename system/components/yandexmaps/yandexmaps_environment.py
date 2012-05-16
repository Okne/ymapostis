
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
Created on 03.02.2010

@author: Andrei Krauchanka
'''

import os
import suit.core.kernel as core

resource_group      =   'yandexmap'
resource_dir        =   os.path.join(os.path.dirname(__file__), "media")

res_tmp_dir        =   os.path.join(resource_dir, 'tmp')

resource_dirs       =   [res_tmp_dir]

templateName = os.path.join(os.path.dirname(__file__), "template.html")
mapFileName = os.path.join(os.path.dirname(__file__), "map.html")
testScript = os.path.join(os.path.dirname(__file__), "script.js")

#api_key = "AJ-8lk8BAAAA-XpFDwQAoJN8eB59A0iz1F1M1tRGnzO-7H0AAAAAAAAAAABMVbn1rJgaBBtgmNsMsBM0CTAf7A=="

#key for localhost
api_key = "AFDNl08BAAAA_xV-XwQAiuknb6WB65sveNpmmQ3SA55fpQgAAAAAAAAAAAC38zKrpEddRzmduhRGZ-QpLCBhuQ=="
