import datetime
from google.appengine.ext import db
import re

class Dedication(db.Model):
    body = db.StringProperty(required=True, multiline=True)
    from_name = db.StringProperty(required=True)
    to_name = db.StringProperty(required=True)
    secret = db.IntegerProperty(required=True)
    deleted = db.BooleanProperty(default=False)
    pub_date = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()

    def iso_date(self):
        return self.pub_date.strftime("%a, %d %b %Y %H:%M:%S +0000")

    def print_date(self):
        return self.pub_date.strftime("%H:%M on %B %d, %Y")

    def link(self):
        name = self.to_name
        return 'http://ijustlovecoffee.com/d/%s/%s/' % (self.key(), name)

class UserPrefs(db.Model):
    user = db.UserProperty(required=True)
    like = db.BooleanProperty(default=False)

class Likes(db.Model):
    value = db.IntegerProperty(required=True)

