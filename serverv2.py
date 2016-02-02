from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from os import curdir, sep, path
import model
class serverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/users"):
                filename=curdir + sep + 'html' + self.path + '.html'
                print filename
                f=open(filename)
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                user=model.Model()
                users=user.get_users()
                data="No Result"
                if users:
                    data=""
                    data="<table>"
                    for u in users:
                        data+= "<tr><td>" + u.name + "</td><td><a href='/show/%s'>show</a></td><td><a href='/edit/%s'>edit</a></td><td><a href='/delete/%s'>delete</a></td></tr>" % (u.id,u.id,u.id)
                    data+="</table>"
                self.wfile.write(f.read() % data)
                f.close()
                return
            if self.path.startswith("/edit"):
                params=self.path.split("/");
                print params
                filename=curdir + sep + 'html' + sep + params[1] + '.html'
                print filename
                f=open(filename)
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                user=model.Model()
                u=user.find_user(params[2])
                data="No Result"
                if user:
                    self.wfile.write(f.read() % (u.id,u.name,u.email,u.phone))
                f.close()
                return             
            if self.path.startswith("/show"):
                params=self.path.split("/");
                print params
                filename=curdir + sep + 'html' + sep + params[1] + '.html'
                print filename
                f=open(filename)
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                user=model.Model()
                u=user.find_user(params[2])
                data="No Result"
                if user:
                    data=""
                    data="<ul>"
                    data+= "<li>Name : %s </li><li>Email : %s </li><li>Phone : %s </li>" % (u.name,u.email,u.phone)                        
                    data+="</ul>"
                self.wfile.write(f.read() % data)
                f.close()
                return                
            else:
                raise IOError        
        except IOError:            
            self.send_error(404,"File not found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/from-data':
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent=fields.get('message')
        except:
            pass
    
if __name__ == '__main__':
        try:
            server = HTTPServer(("localhost", 8888), serverHandler)
            print 'Started httpserver on port 8888'
            server.serve_forever()

        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            server.socket.close()
