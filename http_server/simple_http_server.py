"""
Implementation of simple http-server
"""

import SimpleHTTPServer
import SocketServer
import os
import cgi
import threading
from time import sleep

PORT = 8088
www_folder = os.path.join(os.path.dirname(__file__), "www")
uploaded_folder = os.path.join(www_folder, "uploaded")

httpd = None
ask_user = False

'''
Created on 03.02.2012

@author: Andrei Krauchanka
'''
class MySimpleHttpServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def translate_path(self, path):
        path = SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)
        if path.startswith(os.path.altsep):
            path = os.path.join(uploaded_folder, path[1:])
        return os.path.normpath(path)
    
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
				
				# save uploaded file to disk
                f = open(os.path.join(uploaded_folder, field), "w")
                f.write(file_data)
                f.close()
				
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s (%d bytes)\n' % (field, 
                                                                 file_len))
            else:
                # Regular form value
                self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        return
    
class HttpServerThread(threading.Thread):
    
    def __init__(self, threadName, threadId):
        self.threadName = threadName
        self.threadId = threadId
        threading.Thread.__init__(self)
        
    def run(self):
        print "serving at port ", PORT
        global ask_user 
        ask_user = True
        
        global httpd
        Handler = MySimpleHttpServerHandler
        httpd = SocketServer.TCPServer(("", PORT), Handler)
        httpd.serve_forever()

if __name__ == "__main__":
    
    serverThread = HttpServerThread("http server thread", 1)
    serverThread.start()
    
    #wait for server to start
    while not ask_user:
        sleep(1)        
    
    command = "go"
    while command != "shutdown":
    	command = raw_input("Type 'shutdown' to stop http-server: ")
    
    print "shutdown server at port ", PORT	
    httpd.shutdown()


