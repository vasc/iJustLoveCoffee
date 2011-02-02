from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os
import random
from datetime import datetime
import re
import model
import uuid

def base_host():
    config = ConfigParser.RawConfigParser()
    config.read('globals.cfg')
    return config.get('Web', 'base')

def test_user_pass(user, _pass):
    config = ConfigParser.RawConfigParser()
    config.read('globals.cfg')
    return user == config.get('Admin', 'user') and _pass == config.get('Admin', 'pass')

def mysql_cursor():
    db = MySQLdb.connect(host='localhost', passwd='bica', db='ijlc', user='ijlc')
    return db.cursor(MySQLdb.cursors.DictCursor)

def show_deletion(user, _pass, dedication_template):
    if user and _pass and test_user_pass(user, _pass):
        dedication = Template(dedication_template).safe_substitute({'delete_link': '<a href="/web/ijustlovecoffee/delete/$id/$secret/">delete</a> | '})
    else:
        dedication = Template(dedication_template).safe_substitute({'delete_link': ''})
    return dedication

def get_likes():
    l = model.Likes.get_or_insert(key_name='likes', value=0)
    return l

class Like(webapp.RequestHandler):
    def get(self):
        l = get_likes()
        l.value += 1
        l.put()
        self.redirect('/')

class MainPage(webapp.RequestHandler):
    def get(self, page = 1):
        page = int(page)
        if page < 1:
            page = 1
        self.response.headers['Content-Type'] = 'text/html'
        dedications = db.GqlQuery("SELECT * FROM Dedication WHERE deleted=False ORDER BY pub_date DESC LIMIT 10")
        template_values = {
            'dedications': dedications,
            'likes': get_likes().value,
            }
        if users.is_current_user_admin():
            template_values['delete_links'] = True
        path = os.path.join(os.path.dirname(__file__), 'main.tmpl')
        self.response.out.write(template.render(path, template_values))

class AddDedication(webapp.RequestHandler):
    def post(self):
        if self.request.get('body') and self.request.get('from_name') and self.request.get('to_name'):
            ded = model.Dedication(key_name = str(uuid.uuid4())[:5],
                                   body = self.request.get('body'),
                                   from_name = self.request.get('from_name'),
                                   to_name = self.request.get('to_name'),
                                   secret = random.randint(1000000, 10000000))
            ded.put()
        self.redirect('/')

class Delete(webapp.RequestHandler):
    def get(self, key, secret):
        if users.is_current_user_admin():
            secret = int(secret)
            ded = model.Dedication.get_by_key_name(key)
            if ded and ded.secret == secret:
                ded.deleted = True
                ded.put()
        self.redirect('/')

class SignIn(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/')
        else:
            self.redirect(users.create_login_url('/'))#self.request.uri))

class SignOut(webapp.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url('/'))

class Single(webapp.RequestHandler):
    def get(self, d_id):
        self.response.headers['Content-Type'] = 'text/html'
        #try:
        #    key = db.Key(d_id)
        #except:
        #    self.redirect('/')
        #    return
        single = model.Dedication.get_by_key_name(d_id)
        if not single:
            self.redirect('/')
            return
        path = os.path.join(os.path.dirname(__file__), 'main.tmpl')
        template_values = {
            'single': single,
            'likes': 3,
            }
        if users.is_current_user_admin():
            template_values['delete_links'] = True
        self.response.out.write(template.render(path, template_values))
        #dedication_html = re.sub(r'<3', "<img src='/web/ijustlovecoffee/images/heartinline.png' />", dedication_html)


class Feed(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/rss+xml'
        items = db.GqlQuery("SELECT * FROM Dedication ORDER BY pub_date DESC LIMIT 3")
        template_values = {
            'items': items,
            'link': 'http://ijustlovecoffee.com/feed/',
            'last_build_date': max(items, key=lambda x: x.pub_date)
            }
        path = os.path.join(os.path.dirname(__file__), 'rss.tmpl')
        self.response.out.write(template.render(path, template_values))


def feed(user = None, _pass = None):
    main_file = open('rss_main.tmpl', 'r')
    main = main_file.read()
    item_file = open('rss_items.tmpl', 'r')
    item = item_file.read()
    dedication_file = open('dedication.tmpl', 'r')
    dedication = dedication_file.read()
    dedication = show_deletion(user, _pass, dedication)
    items = ''
    cursor = mysql_cursor()
    cursor.execute("SELECT MAX(pub_date) as time FROM dedications")
    time = cursor.fetchone()['time'].strftime("%a, %d %b %Y %H:%M:%S +0000")
    cursor = mysql_cursor()
    cursor.execute("""SELECT * FROM dedications
                      WHERE deleted=FALSE
                      ORDER BY id DESC
                      LIMIT 0, 25""")
    for row in cursor:
        link = 'http://localhost/d/%s/%s/' % (row['id'], row['_to'])
        values = {'content': Template(dedication).safe_substitute(row), 'link': link}
        values.update(row)
        values['pub_date'] = values['pub_date'].strftime("%a, %d %b %Y %H:%M:%S +0000")
        items += Template(item).safe_substitute(values)
    main = Template(main).safe_substitute(items = items, link = 'http://ijustlovecoffee.com/feed/', time = time)
    send_html(main, 'application/rss+xml')


def edit_dedication(id, secret, _from = None, to = None, dedication = None):
    cursor = mysql_cursor()
    if _from:
        cursor.execute("""UPDATE dedications
                          SET _from=%s
                          WHERE id=%s AND secret=%s""", (_from, id, secret))
    if to:
        cursor.execute("""UPDATE dedications
                          SET to=%s
                          WHERE id=%s AND secret=%s""", (to, id, secret))
    if dedication:
        cursor.execute("""UPDATE dedications
                          SET dedication=%s
                          WHERE id=%s AND secret=%s""", (dedication, id, secret))

def del_dedication(id, secret):
    cursor = mysql_cursor()
    cursor.execute("""UPDATE dedications
                      SET deleted=TRUE
                      WHERE id=%s AND secret=%s""", (id, secret))
    #cursor.execute("DELETE FROM dedications WHERE id=%s AND secret=%s", (id, secret))
    main()


def page_404():
    page_404_file = open('404.tmpl', 'r')
    page_404 = page_404_file.read()
    print 'Status: 404 Not Found'
    send_html(page_404)


def send_html(name, type = "text/html"):
    print 'Content-type: ' + type
    print
    print str(name)

