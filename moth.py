#! /usr/bin/python2

import string
import os
import webapp2
import google.appengine.api.memcache
import google.appengine.ext.ndb

cache = google.appengine.api.memcache.Client()

class Instance(ndb.Model):
    name = ndb.StringProperty()
    

class Page:
    def __init__(self, title, template="template.html"):
        self.title = title
        self.head = []
        self.content = []
        self.stylesheet = 'assets/css/style.css'
        self.icon = 'assets/images/icon.png'
        with open(template) as f:
            self.template = string.Template(f.read())
    
    def write(self, s):
        self.content.append(s)
    
    def __str__(self):
        return self.template.substitute(
              title=self.title,
              stylesheet=self.stylesheet,
              icon=self.icon,
              head="\n".join(self.head),
              content="\n".join(self.content),
        )


class Home(webapp2.RequestHandler):
    def get(self):
        p = Page("Fire Home")
        p.write("Hello, webapp2!")
        self.response.write(p)

    
class Register(webapp2.RequestHandler):
    def get(self):
        p = Page("Teams")
        
        p.write("<pre>")
        cache.add("dink", "merf", time=30)
        p.write("</pre>")


class Puzzler(webapp2.RequestHandler):
    pass



class TokenRedeemer(webapp2.RequestHandler):
    pass


class Static(webapp2.RequestHandler):
    def get(self):
        relpath = self.request.path[1:]
        if relpath.endswith(".html"):
            self.response.content_type = "text/html"
        if relpath.endswith(".css"):
            self.response.content_type = "text/css"
        elif relpath.endswith(".png"):
            self.response.content_type = "image/png"
        elif relpath.endswith(".jpg"):
            self.response.content_type = "image/jpeg"
        else:
            self.response.content_type = "application/octet-stream"
        try:
            with open(relpath) as f:
                self.response.write(f.read())
        except:
            self.response.set_status(404)
            self.response.write("File not found")


class Admin(webapp2.RequestHandler):
    def get(self):
        # For now, just fake a bunch of stuff
        

app = webapp2.WSGIApplication(debug=True)
app.router.add((r"/", Home))
app.router.add((r"/register", Register))
app.router.add((r"/puzzler", Puzzler))
app.router.add((r"/token", TokenRedeemer))
app.router.add((r"/admin", Admin))
app.router.add((r"/.+", Static))

def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='4444')
  
if __name__ == '__main__':
  main()
