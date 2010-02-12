#! /usr/bin/python
 
#routes like dispatcher to work on plain cgi
#request url looks like this 'paths.py?path=/abc/def/ghj/;' after mod_rewrite
 
import re
import cgi
import cgitb
 
def dispatch(path, rules):
    for rule in rules:
        dest = rule['dest']
        r = re.search(rule['re'], path)
        if(r):
            dest(**r.groupdict())
            return
    page_404(path)
 
 
def page_404(path):
    print 'Status: 404 Not Found'
    print 'Content-type: text/plain'
    print
    print '404 ' + str(path)

 
cgitb.enable() 
form = cgi.FieldStorage()

path = ''
if isinstance(form['path'], list):
    path = form['path'][1].value

dispatch(form, [])
