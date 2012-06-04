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

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import blobstore_handlers

class YMapsMLFile(db.Model):
    filename = db.StringProperty()
    blob_key = db.StringProperty()
    
class ViewFileHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, file_key):
        if not blobstore.get(file_key):
            self.error(404)
        else:
            self.send_blob(file_key)

class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            logging.info("trying to upload file(s)")
            for upload in self.get_uploads():
                logging.info("upload file: " + upload.fileName)
                user_photo = YMapsMLFile(filename=upload.filename,
                                       blob_key=upload.key())
                logging.info("save file to blobstore with key: " + upload.key())
                db.put(user_photo)
            
            logging.info("finish uploading")
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, webapp World!')
                
        except:
            self.error(500)

app = webapp.WSGIApplication([('/file/(.*)', ViewFileHandler),
                               ('/upload', FileUploadHandler)],
                              debug=True)
                              
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(app)

if __name__ == "__main__":
    main()

