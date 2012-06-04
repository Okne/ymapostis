#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import cgi

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import blobstore_handlers

class YMapsMLFile(db.Model):
    filename = db.StringProperty()
    content = db.TextProperty()
    
class ViewFileHandler(webapp.RequestHandler):
    def get(self, file_name):
        self.response.headers.add_header('Content-Type', 'application/atom+xml; charset=\"UTF-8\"')
        file_info = YMapsMLFile.gql("where filename=:1", file_name).get()
        if file_info is not None:
            self.response.out.write(file_info.content.encode("cp1251"))
        else:
            self.response.set_status(404)

class FileUploadHandler(webapp.RequestHandler):
    def post(self):
        # Parse the form data posted
        file_name = self.request.get("filename")
        file_data = self.request.body
        file_data = file_data.decode("unicode-escape")

        #self.response.out.write('Client: %s\n' % str(self.request.remote_addr))
        #self.response.out.write('Path: %s\n' % self.request.path)
        #self.response.out.write('Form data:\n')

        # Echo back information about what was posted in the form
        
        ymaps_file = None        
        file_info = YMapsMLFile.gql("where filename=:1", file_name).get()
        if file_info is not None:
            ymaps_file = file_info
            ymaps_file.content = file_data
        else:
            ymaps_file = YMapsMLFile(filename=file_name, content=file_data)
        
        db.put(ymaps_file)
                
        file_len = len(file_data)
        del file_data
        self.response.out.write('\tUploaded %s (%d bytes)\n' % (file_name, 
                                                                 file_len))

app = webapp.WSGIApplication([('/file/(.*)', ViewFileHandler),
                               ('/upload', FileUploadHandler)],
                              debug=True)
                              
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(app)

if __name__ == "__main__":
    main()

