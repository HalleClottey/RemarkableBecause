import webapp2
import jinja2
import os
from google.appengine.api import urlfetch
import json
from google.appengine.api import users
import random
from google.appengine.ext import ndb
import datetime
# import api_key.py

def root_parent():
    '''A single key to be used as the ancestor for all dog entries.
    Allows for strong consistency at the cost of scalability.'''
    return ndb.Key('Parent', 'default_parent')

class Remarkable(ndb.Model):
    '''A database entry representing why they're remarkable.'''
    user = ndb.UserProperty()
    remarkable_because = ndb.StringProperty()
    date = ndb.StringProperty() #Date property

class Diary_Entry(ndb.Model):
    user = ndb.UserProperty()
    entry = ndb.StringProperty()
    date = ndb.StringProperty()

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

class MainPageUser(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/homepageuser.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class Resources_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/resources.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class Quotes_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/Quotes.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class Diary_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/Diary.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'entries': Diary_Entry.query(Diary_Entry.user == user, ancestor=root_parent()).fetch()
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class New_Diary_Entry_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/NewDiaryEntry.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'today': datetime.datetime.now().strftime("%B %d, %Y"),

        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
    def post(self):
        user = users.get_current_user()
        new_entry = Diary_Entry(parent=root_parent())
        new_entry.entry = self.request.get('diary_post')
        new_entry.user = user
        new_entry.date = datetime.datetime.now().strftime("%B %d, %Y")
        new_entry.put()
        self.redirect('/diary')

class Calendar_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/Calendar.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        thirty_one = {}
        for i in range(1,32):
            thirty_one[i] = i
        thirty = {}
        for i in range(1,31):
            thirty[i] = i
        february = {}
        for i in range(1,29):
            february[i] = i
        times = "Current date: %s/%s/%s" % (datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().year)
        #dates = database.remarkable.query(database.StoredDate.username == user.nickname()).fetch()
        date_remarkables = Remarkable.query()
        #date_remarkables=date_remarkables.filter("user==",user.nickname())
        user_date="may 22nd 2019"
        #date_remarkables=date_remarkables.filter(Remarkable.date=user_date)
        print('your user name')
        items=date_remarkables.fetch()
        print(items)
        # values = {
        #     'time': times,
        #     #'storedDate':date,
        #     'jan': thirty_one,
        #     'feb': february,
        #     'mar': thirty_one,
        #      'apr': thirty,
        #      'may': thirty_one,
        #      'june': thirty,
        #      'july': thirty_one,
        #      'aug': thirty_one,
        #      'sep': thirty,
        #      'oct': thirty_one,
        #      'nov': thirty,
        #      'dec': thirty_one,
        # }
        # self.response.headers['Content-Type'] = 'text/html'
        # self.response.write(template.render(data))

class Help_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/Help.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class Remarkable_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/remarkable.html')
        all_remarkables = Remarkable.query(ancestor=root_parent()).fetch()
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'i_am_remarkable_because': random.choice(all_remarkables),
          'today': datetime.datetime.now().strftime("%B %d, %Y"),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


    def post(self):
        user = users.get_current_user()
        new_response = Remarkable(parent=root_parent())
        new_response.date = datetime.datetime.now().strftime("%B %d, %Y")
        new_response.remarkable_because = self.request.get('remarkable_post')
        new_response.put()
        self.redirect('/thankyou')

class Thank_You_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/thankyou.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class Test_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/test.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/home', MainPageUser),
    ('/resources',Resources_Handler),
    ('/motivation',Quotes_Handler),
    ('/diary',Diary_Handler),
    ('/diaryentry',New_Diary_Entry_Handler),
    ('/calendar',Calendar_Handler),
    ('/remarkable',Remarkable_Handler),
    ('/help',Help_Handler),
    ('/thankyou',Thank_You_Handler),
    ('/test', Test_Handler)
], debug=True)
