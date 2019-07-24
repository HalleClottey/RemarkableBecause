import webapp2
import jinja2
import os
from google.appengine.api import urlfetch
import json
from google.appengine.api import users
import random
from google.appengine.ext import ndb
import datetime
import api_key

#function to retrieve quotes from the api
def getQuotes():

  headers={
    "X-RapidAPI-Host": "healthruwords.p.rapidapi.com",
    "X-RapidAPI-Key": api_key.rapidapi_key
  }

  quotes_api_url= "https://healthruwords.p.rapidapi.com/v1/quotes/?size=medium"
  quotes_response = urlfetch.fetch(url = quotes_api_url, headers = headers).content
  quotes_json = json.loads(quotes_response)
  all_quotes = {}

  return quotes_json
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
    # counter = ndb.IntegerProperty()

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



#class that retrieves and pulls quotes from the API
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

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENVIRONMENT.get_template('Template/Quotes.html')
        self.response.write(index_template.render({'message':getQuotes()}))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENVIRONMENT.get_template('Template/Quotes.html')
        self.response.write(index_template.render({'message':getQuotes()}))



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
        # new_entry.counter =
        new_entry.put()
        self.redirect('/diary')

class Display_Diary_Entry_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        entry_key = ndb.Key(urlsafe=self.request.get('entry_key'))
        diary_entry = entry_key.get()
        template = JINJA_ENVIRONMENT.get_template('Template/DisplayDiaryEntry.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'entry': diary_entry,
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class Calendar_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/Calendar.html')
        # date_key = ndb.Key(urlsafe==self.request.get('date_key'))
        # date_entry = date_key.get()
        dates=range(1,32)
        remarkables=Remarkable.query(Remarkable.user == user, ancestor=root_parent()).fetch()
        remarkables_dates=[]
        for remarkable in remarkables:
            if remarkable.date not in remarkables_dates:
                remarkables_dates.append(remarkable.date)
        print(remarkables_dates)
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'dates':dates
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

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
        all_remarkables = Remarkable.query(Remarkable.user == user, ancestor=root_parent()).fetch()
        prefix = ""
        suffix = ""
        default_remarkables = ['I woke up today.', 'I found the energy to log onto this site.']
        if all_remarkables:
            my_remarkable = random.choice(all_remarkables).remarkable_because
            prefix = "On " + datetime.datetime.now().strftime("%B %d, %Y") + ", you wrote: "
        else:
            my_remarkable = random.choice(default_remarkables)
            suffix = " ~ The Remarkable Staff ~"
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'i_am_remarkable_because': my_remarkable,
          'today': datetime.datetime.now().strftime("%B %d, %Y"),
          'prefix': prefix,
          'suffix': suffix,
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


    def post(self):
        user = users.get_current_user()
        new_response = Remarkable(parent=root_parent())
        new_response.user = user
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

class Login_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('Template/login.html')
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
    ('/resources', Resources_Handler),
    ('/motivation', Quotes_Handler),
    ('/diary', Diary_Handler),
    ('/diaryentry', New_Diary_Entry_Handler),
    ('/display_diary_entry', Display_Diary_Entry_Handler),
    ('/calendar', Calendar_Handler),
    ('/remarkable', Remarkable_Handler),
    ('/help', Help_Handler),
    ('/thankyou', Thank_You_Handler),
    ('/test', Test_Handler),
    ('/login', Login_Handler)

], debug=True)
