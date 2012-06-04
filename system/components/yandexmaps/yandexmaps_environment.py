
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
import urllib2

resource_group      =   'yandexmap'
resource_dir        =   os.path.join(os.path.dirname(__file__), "media")

res_tmp_dir        =   os.path.join(resource_dir, 'tmp')

resource_dirs       =   [res_tmp_dir]

templateName = os.path.join(os.path.dirname(__file__), "template.html")
mapFileName = os.path.join(os.path.dirname(__file__), "map.html")
testData = os.path.join(os.path.dirname(__file__), "testData.xml")
wwwDir = os.path.join(os.path.dirname(__file__), "www")
uploadedDir = os.path.join(wwwDir, "uploaded")
#server_address = "http://195.50.17.209:8088/"
#server_address = "http://178.121.178.213:8088/"
#server_address = "http://127.0.0.1:8088"
server_address = "http://ymapserver.appspot.com"

is_proxy = False
http_proxy_server = "someproxyserver.com"
http_proxy_port = "8080"
http_proxy_user = "username"
http_proxy_passwd = "password"

# Next line = "http://username:password@someproxyserver.com:8080"
http_proxy_full_auth_string = "http://%s:%s@%s:%s" % (http_proxy_user,
                                                      http_proxy_passwd,
                                                      http_proxy_server,
                                                      http_proxy_port)



#api_key = "AJ-8lk8BAAAA-XpFDwQAoJN8eB59A0iz1F1M1tRGnzO-7H0AAAAAAAAAAABMVbn1rJgaBBtgmNsMsBM0CTAf7A=="

#key for localhost
api_key = "AFDNl08BAAAA_xV-XwQAiuknb6WB65sveNpmmQ3SA55fpQgAAAAAAAAAAAC38zKrpEddRzmduhRGZ-QpLCBhuQ=="
