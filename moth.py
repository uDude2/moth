#! /usr/bin/python2

import string
import time
import webapp2
import json
import logging
from google.appengine.ext import ndb


class Instance(ndb.Model):
    enabled = ndb.BooleanProperty()
    name = ndb.StringProperty()
    categories = ndb.StringProperty(repeated=True)
    teams = ndb.JsonProperty()
    events = ndb.JsonProperty()
    messages = ndb.StringProperty(repeated=True)

def get_instance(name):
    key = ndb.Key("Instance", name)
    instance = key.get()
    return key.get()

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

class MothRequestHandler(webapp2.RequestHandler):
    def error(self, message, code=500):
        response.write(message)
        response.set_status(code)


class Home(MothRequestHandler):
    def get(self):
        p = Page("Fire Home")
        p.write("Hello, webapp2!")
        self.response.write(p)

    
class Register(MothRequestHandler):
    def get(self):
        p = Page("Teams")
        
        p.write("<pre>")
        cache.add("dink", "merf", time=30)
        p.write("</pre>")


class Puzzler(MothRequestHandler):
    pass


class State(MothRequestHandler):
    """Dump instance state"""
    def get(self):
        instanceName = self.request.get("instance")
        teamId = self.request.get("teamid")
        if not instanceName or not teamId:
            return self.error("Invalid Arguments", 403)
        instance = get_instance(instanceName)
        if not instance:
            return self.error("No such instance", 403)
        teamName = instance.teams.get(teamId)
        if not teamName:
            return self.error("I don't recognize that team", 403)

        teams = {}
        nteams = 0
        events = []
        teamNames = []
        for event in instance.events:
            token = event[1]
            teamNo = teams.get(token)
            if teamNo is None:
                teamNo = nteams
                teams[token] = teamNo
                teamNames.append(instance.teams[token])
                nteams += 1
            event[1] = teamNo
            events.append(event)

        bigObject = {
            "name": instance.name,
            "teams": teamNames,
            "puzzles": "XXX: Complete this",
            "events": events,
            "messages": instance.messages,
        }
        json.dump(bigObject, self.response, separators=(',',':'))
        self.response.content_type = "application/json"


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
        pass

class Debug(webapp2.RequestHandler):
    def get(self):
        name = "bubbles"
        instance = get_instance(name)
        if not instance:
            self.response.write("<p>Making new instance</p>")
            instance = Instance(id=name)
            instance.name = name
            instance.enabled = False
            instance.categories = ["addition"]
            instance.teams = {"a1b2c3d4": "Team Rabbit"}
            instance.events = []
        event = (int(time.time()), "a1b2c3d4", "addition", 58)
        instance.events.append(event)
        instance.put()
        self.response.write(instance)

app = webapp2.WSGIApplication(debug=True)
app.router.add((r"/", Home))
app.router.add((r"/register", Register))
app.router.add((r"/puzzler", Puzzler))
app.router.add((r"/state", State))
app.router.add((r"/admin", Admin))
app.router.add((r"/debug", Debug))
app.router.add((r"/.+", Static))

def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='4444')
  
if __name__ == '__main__':
  main()
