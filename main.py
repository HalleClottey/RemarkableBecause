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
import calendar

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
    real_date= ndb.DateProperty()

class Diary_Entry(ndb.Model):
    user = ndb.UserProperty()
    entry = ndb.StringProperty()
    date = ndb.StringProperty()
    subject = ndb.StringProperty()
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
        template = JINJA_ENVIRONMENT.get_template('template/homePageOne.html')
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
        template = JINJA_ENVIRONMENT.get_template('template/homepageuser.html')
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
        template = JINJA_ENVIRONMENT.get_template('template/resources.html')
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
        print user
        template = JINJA_ENVIRONMENT.get_template('template/Quotes.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'message':getQuotes(),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

    # def get(self):
    #     self.response.headers['Content-Type'] = 'text/html'
    #     index_template = JINJA_ENVIRONMENT.get_template('template/Quotes.html')
    #     self.response.write(index_template.render({'message':getQuotes()}))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENVIRONMENT.get_template('template/Quotes.html')
        self.response.write(index_template.render({'message':getQuotes()}))



class Diary_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('template/Diary.html')
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
        template = JINJA_ENVIRONMENT.get_template('template/NewDiaryEntry.html')
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
        new_entry.subject = self.request.get('subject_post')
        # new_entry.counter =
        new_entry.put()
        self.redirect('/diary')

class Display_Diary_Entry_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        entry_key = ndb.Key(urlsafe=self.request.get('entry_key'))
        diary_entry = entry_key.get()
        template = JINJA_ENVIRONMENT.get_template('template/DisplayDiaryEntry.html')
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
        template = JINJA_ENVIRONMENT.get_template('template/Calendar.html')
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        remarkables=Remarkable.query(Remarkable.user == user, ancestor=root_parent()).fetch()
        remarkables_dates=[]

        for remarkable in remarkables:
            if remarkable.real_date is not None:
                if remarkable.real_date.year == year and remarkable.real_date.month==month:
                    if remarkable.real_date not in remarkables_dates:
                        remarkables_dates.append(remarkable.real_date.day)
        print(remarkables_dates)
        calendar_param= self.request.get('calendar_param')
        month_range=calendar.monthrange(year,month)
        List_months=['January','February','March','April','May','June','July','August','September','November','December']
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'start_date': month_range[0],
          'last_day':month_range[1],
          'year':year,
          'month':List_months[month-1],
          'remarkables_dates':remarkables_dates
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

    def post(self):
        displayDay = self.request.get('date')
        if displayDay == "":
            self.redirect("/calendar")
            return
        foo=datetime.datetime.strptime(displayDay,'%Y-%m-%d')
        reformated_day=foo.strftime('%B %d, %Y')

        #print(displayDay.strftime("%B %d, %Y"))
        self.redirect("/calendar_item?day=%s" % reformated_day)
        print("hello")


class Calendar_Item_Handler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('template/calendar_item.html')
        displayDay = self.request.get('day')
        all_remarkables = Remarkable.query(Remarkable.user == user, ancestor=root_parent()).filter(ndb.GenericProperty("date") == displayDay).fetch()
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'all_remarkables':all_remarkables,
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
        print("hi")
        print(displayDay)
        print(all_remarkables)

class Help_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('template/Help.html')
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
        template = JINJA_ENVIRONMENT.get_template('template/remarkable.html')
        all_remarkables = Remarkable.query(Remarkable.user == user, ancestor=root_parent()).fetch()
        prefix = ""
        suffix = ""
        today = ""
        my_remarkable_response = ""
        my_remarkable_date = ""
        default_remarkables = ['I woke up today.', 'I found the energy to log onto this site.', 'I am flawless.', 'I woke up like this.', 'I am beautiful!']
        if all_remarkables:
            #Can also use my_remarkable.PROPERTY to retrieve any property from Remarkable class
            my_remarkable = random.choice(all_remarkables)
            my_remarkable_response = my_remarkable.remarkable_because
            my_remarkable_date = my_remarkable.date
            prefix = "On " + my_remarkable_date + ", you wrote: "
        else:
            my_remarkable_response = random.choice(default_remarkables)
            suffix = " ~ The Remarkable Staff ~"
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url('/'),
          'i_am_remarkable_because': my_remarkable_response,
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
        new_response.real_date=datetime.datetime.now()
        new_response.put()
        self.redirect('/thankyou')

class Thank_You_Handler(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('template/thankyou.html')
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
        template = JINJA_ENVIRONMENT.get_template('template/test.html')
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
        template = JINJA_ENVIRONMENT.get_template('template/login.html')
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
    ('/calendar_item',Calendar_Item_Handler),
    ('/remarkable', Remarkable_Handler),
    ('/help', Help_Handler),
    ('/thankyou', Thank_You_Handler),
    ('/test', Test_Handler),
    ('/login', Login_Handler)

], debug=True)
