import webapp2
import jinja2
import os
from google.appengine.api import urlfetch
import json
from google.appengine.api import users


# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    # def get(self): #for a get request
    #     self.response.headers['Content-Type'] = 'text/html'
    #     index_template = JINJA_ENV.get_template('templates/homePageOne.html')
    #     values = {'clues': get_random_clues(5)}
    #     self.response.write(index_template.render(values))
    #     #print("Hello")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
