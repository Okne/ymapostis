# -*- coding: utf-8 -*-
#!/usr/bin/python

'''
Created on 09.06.2010
Copyright (C) 2010 Alexander S. Razzhivin ( site http://httpbots.com )

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see .
'''

import socket
import sys
import threading
import os
import errno

shutdown = False
ROOTDIR = "./www"

class HttpServerThread(threading.Thread):
    def __init__(self, threadName, threadId):
        self.threadName = threadName
        self.threadId = threadId
        threading.Thread.__init__(self)
    
    def run(self):
        print "Start " + self.threadName
        init_server()
        print "Finish " + self.threadName

def send_string(socket, data):
    """
    Эта функция гарантирует отсылку всех байтов строки
    """
    bytes_to_send = len(data)
    while bytes_to_send > 0:
        sent_bytes = socket.send(data, bytes_to_send)
        if sent_bytes == -1:
            return False;
        bytes_to_send -= sent_bytes
    return True
    
def recv_line(socket):
    """
    Эта функция получает из открытого сокета строка пока не встретиться конец строки EOL
    Возвращает строку и длину строки в виде кортежа (строка, длина)
    """
    EOL = "\r\n"
    nbytes = 1
    buffer = socket.recv(nbytes)

    while not EOL in buffer:
        buffer += socket.recv(nbytes)
    result = buffer[:-2]
    return (result, len(result))


def process_connetion(sock, address):
    
    request, length = recv_line(sock)
    print 'Got request from %s:%d "%s" \n' % (address[0], address[1], request)
  
    if " HTTP/" in request:
        file_path = None
        if "GET " in request:
            file_path = request[4:-9]
        if "HEAD " in request:
            file_path = request[5:-9]
        if file_path:
            if file_path == '/':
                file_path = '/index.html'
            resource = ROOTDIR
            resource += file_path
            try:
                f = open(resource, 'rb')
                print " 200 OK\n"
                send_string(sock, "HTTP/1.0 200 OK\r\n")
                send_string(sock, "Content-Type: text/html; charset=UTF-8\r\n")
                send_string(sock, "Set-Cookie: name=value\r\n") # установим куки
                send_string(sock, "Server: Nano PyHttpd\r\n\r\n")
                if "GET " in request:
                    file_content = f.read()
                    sock.send(file_content, 10485760) # возникает проблема с отправкой больших файлов
   
                f.close()
            except IOError as error:                
                print os.strerror(error.errno)
                print errno.errorcode[error.errno]
                print " 404 Not found\n"
                send_string(sock, "HTTP/1.0 404 NOT FOUND\r\n")
                send_string(sock, "Server: Nano PyHttpd\r\n\r\n")
                send_string(sock, "404 Not Found")
                send_string(sock, "URL not found\r\n")
        
        else:
            print "\tUnknown request!\n" # Если тип запроса не известен
    else:
        print " NOT HTTP!\n"
    sock.shutdown(socket.SHUT_RD) # корректно закрыть сокет
    sock.close()

def init_server():
    host = ''
    port = 8088
    backlog = 1
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http_socket.bind((host, port))
    http_socket.listen(backlog)
    while not shutdown:
        client, address = http_socket.accept()
        process_connetion(client, address)
        
if __name__ == "__main__":
    server_thread = HttpServerThread("Nano http-server", 1)
    server_thread.start()
