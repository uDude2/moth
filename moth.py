#! /usr/bin/python2

import string
import webapp2

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
  pass

class Puzzler(webapp2.RequestHandler):
  pass

class TokenRedeemer(webapp2.RequestHandler):
  pass

class Static(webapp2.RequestHandler):
  def get(self):
    print(dir(self.response.headers))
    relpath = self.request.path[1:]
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

app = webapp2.WSGIApplication(debug=True)
app.router.add((r"/", Home))
app.router.add((r"/register", Register))
app.router.add((r"/puzzler", Puzzler))
app.router.add((r"/token", TokenRedeemer))
app.router.add((r"/.+", Static))

def main():
  from paste import httpserver
  httpserver.serve(app, host='0.0.0.0', port='4444')
  
if __name__ == '__main__':
  main()
