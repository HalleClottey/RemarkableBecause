import webapp2
import jinja2
import os
from google.appengine.api import urlfetch
import json
from google.appengine.api import users


# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/homePageOne.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
