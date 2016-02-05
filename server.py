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
            if self.path.endswith("/create"):
                filename=curdir + sep + 'html' + self.path + '.html'
                print filename
                f=open(filename)
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(f.read())
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
                if user:
                    self.wfile.write(f.read() % (u.id,u.name,u.email,u.phone))
                else:
                    self.wfile.write("Nothing to edit")
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
                if u:
                    self.wfile.write(f.read() % (u.name,u.email,u.phone))
                else:
                    self.wfile.write("No user find to show")
                f.close()
                return
            if self.path.startswith("/delete"):
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
                if u:
                    self.wfile.write(f.read() % (u.name,u.id,u.name))
                else:
                    self.wfile.write("No user find to show")
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
            if self.path.endswith("/update"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))                        
                if ctype == 'multipart/form-data':                
                    fields=cgi.parse_multipart(self.rfile, pdict)                                                                    
                    user=model.Model()                    
                    user.update_user({
                        "id" : fields['id'][0],
                        "email" : fields['email'][0],
                        "phone" : fields['phone'][0],
                        "name" : fields['name'][0]
                    })
                    self.wfile.write("<html><head><title>redirect</title><body>click <a href='/show/%s'>here</a> to go back</body></html>" % fields['id'][0])
            if self.path.endswith("/do_create"):
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type']}
                )
                print form
                user=model.Model()
                user.create_user(form)
                self.wfile.write("<html><head><title>redirect</title><body>User %s created with success.<br/>Click <a href='/users'>here</a> to go back</body></html>" % form.getvalue('name'))
            if self.path.endswith("/confirm_delete"):
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'DELETE','CONTENT_TYPE':self.headers['Content-Type']}
                )                
                user=model.Model()
                user.delete_user(form['id'].value)
                self.wfile.write("<html><head><title>redirect</title><body>User %s deleted success.<br/>Click <a href='/users'>here</a> to go back</body></html>" % form.getvalue('name'))
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
