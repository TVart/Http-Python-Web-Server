#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi

PORT_NUMBER = 8080
HOST_NAME   = '192.168.0.50'
VALID_PAGES = {
		"/index": "/index.html",
                "/notfound": "/introduction.html"
}
DEFAULT_PAGE = "/index.html"

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):
	def do_RESPONSE(self,form):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
        	self.wfile.write("<html><head><title>Title goes here.</title></head>")
		if "name" not in form or "addr" not in form:
		    print "<H1>Error</H1>"
		    print "Please fill in the name and addr fields."
                    self.wfile.write("Please fill you name and your address")
		else :
		    print "<p>name:", form["name"].value
		    print "<p>addr:", form["addr"].value
                    self.wfile.write("Hello %s !\n" % form["name"].value)
                    self.wfile.write("You live in %s !" % form["addr"].value)
#        	     self.wfile.write("Hello %s ! \r\nYou live in %s" % form['name'].value form['addr'].value)
                    self.wfile.write("</body></html>")		
        	self.wfile.write("</body></html>")		
		return

        #Handler for the HEAD requests
        def do_HEAD(self):
	        self.send_response(200)
		self.send_header("Content-type", "text/html")
                self.end_headers()

        #Handler for the POST requests
        def do_POST(self):
                if self.path=="/send":
                        form = cgi.FieldStorage(
                                fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                 'CONTENT_TYPE':self.headers['Content-Type'],
                        })

			self.do_RESPONSE(form)
                        return

	#Handler for the GET requests
	def do_GET(self):
                self.path = VALID_PAGES.get(self.path, DEFAULT_PAGE)
                try:
                        #Check the file extension required and
                        #set the right mime type

                        sendReply = False
                        if self.path.endswith(".html"):
                                mimetype='text/html'
                                sendReply = True
                        if self.path.endswith(".jpg"):
                                mimetype='image/jpg'
                                sendReply = True
                        if self.path.endswith(".gif"):
                                mimetype='image/gif'
                                sendReply = True
                        if self.path.endswith(".js"):
                                mimetype='application/javascript'
                                sendReply = True
                        if self.path.endswith(".css"):
                                mimetype='text/css'
                                sendReply = True

                        if sendReply == True:
                                #Open the static file requested and send it
                                f = open(curdir + sep + self.path)
                                self.send_response(200)
                                self.send_header('Content-type',mimetype)
                                self.end_headers()
                                self.wfile.write(f.read())
                                f.close()
                        return
		
                except IOError:
                        self.send_error(404,'File Not Found: %s' % self.path)


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer((HOST_NAME, PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
