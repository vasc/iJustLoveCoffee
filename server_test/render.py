from string import Template
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
try:
   import MySQLdb
except ImportError as ie:
   print str(ie)

#import random
#import ConfigParser
#from datetime import datetime

#def base_host():
#    config = ConfigParser.RawConfigParser()
#    config.read('globals.cfg')
#    return config.get('Web', 'base')

#def test_user_pass(user, _pass):
#    config = ConfigParser.RawConfigParser()
#    config.read('globals.cfg')
#    return user == config.get('Admin', 'user') and _pass == config.get('Admin', 'pass')

#def mysql_cursor():
#    db = MySQLdb.connect(host='localhost', passwd='bica', db='ijlc', user='ijlc')
#    return db.cursor(MySQLdb.cursors.DictCursor)

#def show_deletion(user, _pass, dedication_template):
#    if user and _pass and test_user_pass(user, _pass):
#        dedication = Template(dedication_template).safe_substitute({'delete_link': '<a href="/web/ijustlovecoffee/delete/$id/$secret/">delete</a> | '})
#    else:
#        dedication = Template(dedication_template).safe_substitute({'delete_link': ''})
#    return dedication


#def main(page = 1, user = None, _pass = None):
#    if not isinstance(page, int) or page < 1:
#        page = 1
#    main_file = open('main.tmpl', 'r')
#    main = main_file.read()
#    dedication_file = open('dedication.tmpl', 'r')
#    dedication = dedication_file.read()
#    dedication = show_deletion(user, _pass, dedication)
#    cursor = mysql_cursor()    
#    limit = ((page-1)*10,)
#    cursor.execute("""SELECT * FROM dedications 
#                      WHERE deleted=FALSE
#                      ORDER BY id DESC
#                      LIMIT %s, 10""", limit)
#    dedications = ''
#    for row in cursor:
#        dedications += Template(dedication).safe_substitute(row)

#    main = Template(main).safe_substitute(dedications = dedications, single = '')
#    send_html(main)


#def single(d_id):
#    main_file = open('main.tmpl', 'r')
#    main = main_file.read()
#    dedication_file = open('dedication.tmpl', 'r')
#    dedication = dedication_file.read()
#    cursor = mysql_cursor()
#    cursor.execute("SELECT * FROM dedications WHERE id = %s", d_id)
#    dedication_html = Template(dedication).safe_substitute(cursor.fetchone())
#    main_html = Template(main).safe_substitute(dedications = '', single = dedication_html)
#    send_html(main_html)


#def feed(user = None, _pass = None):
#    main_file = open('rss_main.tmpl', 'r')
#    main = main_file.read()
#    item_file = open('rss_items.tmpl', 'r')
#    item = item_file.read()    
#    dedication_file = open('dedication.tmpl', 'r')
#    dedication = dedication_file.read()
#    dedication = show_deletion(user, _pass, dedication)
#    items = ''
#    cursor = mysql_cursor()
#    cursor.execute("SELECT MAX(pub_date) as time FROM dedications")
#    time = cursor.fetchone()['time'].strftime("%a, %d %b %Y %H:%M:%S +0000")
#    cursor = mysql_cursor() 
#    cursor.execute("""SELECT * FROM dedications 
#                      WHERE deleted=FALSE
#                      ORDER BY id DESC
#                      LIMIT 0, 25""")
#    for row in cursor:
#        link = 'http://localhost/d/%s/%s/' % (row['id'], row['_to']) 
#        values = {'content': Template(dedication).safe_substitute(row), 'link': link}
#        values.update(row)
#        values['pub_date'] = values['pub_date'].strftime("%a, %d %b %Y %H:%M:%S +0000")
#        items += Template(item).safe_substitute(values)
#    main = Template(main).safe_substitute(items = items, link = 'http://ijustlovecoffee.com/feed/', time = time)
#    send_html(main, 'application/rss+xml')



#def add_dedication(_from, to, dedication):
#    r = random.randint(1000000, 10000000)
#    cursor = mysql_cursor()
#    cursor.execute("INSERT INTO dedications (_from, _to, dedication, secret, pub_date)  Values (%s, %s, %s, %s, NOW())", (_from, to, dedication, r))
#    send_html(cursor)


#def del_dedication(id, secret):
#    cursor = mysql_cursor()
#    cursor.execute("""UPDATE dedications
#                      SET deleted=TRUE
#                      WHERE id=%s AND secret=%s""", (id, secret))
#    #cursor.execute("DELETE FROM dedications WHERE id=%s AND secret=%s", (id, secret))
#    main()


#def page_404():
#    page_404_file = open('404.tmpl', 'r')
#    page_404 = page_404_file.read()
#    print 'Status: 404 Not Found'
#    send_html(page_404)

#    
#def send_html(name, type = "text/html"):
#    print 'Content-type: ' + type
#    print
#    print str(name)
