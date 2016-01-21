#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, path
import cgi
from classes import users
class myServer(BaseHTTPRequestHandler):
    """Render the view"""
    def do_RESPONSE(self,form):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("<html><head><title>Title goes here.</title></head>")
        #self.wfile.write(form)
        if "name" not in form or "addr" not in form:
            print "<H1>Error</H1>"
            print "Please fill in the name and addr fields."
            self.wfile.write("Please fill you name and your address")
        else :
            print "<p>name:", form["name"].value
            print "<p>addr:", form["addr"].value
            self.wfile.write("Hello %s !\n" % form["name"].value)
            self.wfile.write("You live in %s !" % form["addr"].value)
            self.wfile.write("</body></html>")
            self.wfile.write("</body></html>")
        return

    #Handler for the HEAD requests
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_REPLY(self,path):
        sendReply = False
        if path.endswith(".html"):
            mimetype='text/html'
            sendReply = True
        if path.endswith(".jpg"):
            mimetype='image/jpg'
            sendReply = True
        if path.endswith(".gif"):
            mimetype='image/gif'
            sendReply = True
        if path.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        if path.endswith(".css"):
            mimetype='text/css'
            sendReply = True
        return sendReply, mimetype

    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/send":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type']}
            )
            self.do_RESPONSE(form)
        return

    #Handler for the GET requests
    def do_GET(self):
        ressources = {
            '/' : 'views/index.html',
            '/users' : 'views/users.html'
        };
        try:
            u= users.User();
            #first_name, last_name = "tootoo","tiitii";
            #Check the file extension required and set the right mime type
            sendReply = self.do_REPLY(ressources[self.path])

            if sendReply[0] == True:
                f = open(curdir + sep + ressources[self.path])
                self.send_response(200)
                self.send_header('Content-type',sendReply[1])
                self.end_headers()
                self.wfile.write("Requested URI is %s" % self.path)
                self.wfile.write(
                    f.read() % u.all()
                )
                f.close()
            return
        except KeyError:
            self.send_error(404,'File Not Found: %s' % self.path)
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

if __name__ == '__main__':
        try:
            server = HTTPServer(("localhost", 8888), myServer)
            print 'Started httpserver on port 8888'

            server.serve_forever()

        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            server.socket.close()