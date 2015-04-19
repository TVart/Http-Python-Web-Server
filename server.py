#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, path
from jinja2 import Template
from app.controllers import articles as tototo
import cgi

class server(BaseHTTPRequestHandler):
    articles = list()
    """Render the view"""
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
            self.wfile.write("</body></html>")
            self.wfile.write("</body></html>")
        return

    #Handler for the HEAD requests
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_REPLY(self):
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
        route = str(self.path).split('/')
        if(route.__len__() > 2):
            controller = route[0]
            action = route[1]
            params = route[3]
        else:
            controller = route[0]
            action = route[1]
            params = 1

        if(action == ''):
            action = 'list'

        to = tototo.Articles()
        c = {
            "author": "tvart",
            "title" : "My 2nd article",
            "text"  : "Hello world!\nMy first blog post!",
            "tags"  : ["mongodb", "python", "pymongo"],
            "date"  : ""
        }
        actions = {
                'list'  : to.getAll(page=1),
                'show'  : to.getOne(params),
                'new'   : to.create(c),
                'edit'  : to.getOne(params)
        }

        data = actions[str(action)]

        for r in data:
            self.articles.append(r)

        if str(self.path)=="/":
            self.path = "/app/views/index.html"
        else:
            self.path = "/app/views"+self.path+".html"
        print self.path
        try:
            #Check the file extension required and set the right mime type
            sendReply = self.do_REPLY()

            if sendReply[0] == True:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type',sendReply[1])
                self.end_headers()
                template = Template(f.read())
                render = template.render(articles=self.articles,varbidon="Projekt")
                self.wfile.write(render)
                f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

if __name__ == '__main__':
        try:
            #Create a web server and define the handler to manage the
            #incoming request
            server = HTTPServer(("localhost", 8080), server)
            print 'Started httpserver on port 8080'

            #Wait forever for incoming htto requests
            server.serve_forever()

        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            server.socket.close()