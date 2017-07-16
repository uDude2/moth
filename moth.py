#! /usr/bin/python2

import string
import MySQLdb
import os
import webapp2

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db


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
		db = connect_to_cloudsql()
		db.select_db("moth_spark")
		cursor = db.cursor()
		cursor.execute("select * from teams")
		for r in cursor.fetchall():
			p.write("{}\n".format(r))
			
		self.response.write(p)


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
