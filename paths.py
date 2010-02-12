#! /usr/bin/python
 
#routes like dispatcher to work on plain cgi
#request url looks like this 'paths.py?path=/abc/def/ghj/;' after mod_rewrite
 
import re
import cgi
import cgitb
import render
 
def dispatch(path, rules):
    for rule in rules:
        dest = rule['dest']
        r = re.search(rule['re'], path)
        if(r):
            dest(**r.groupdict())
            return
    render.page_404()
 
 
cgitb.enable() 
form = cgi.FieldStorage()
path = ''
if 'path' in form:
    path = form['path'].value

rules = [ {'re': r'^$', 'dest': render.main},
          {'re': r'^page/(?P<page>\d+)', 'dest': render.main},
          {'re': r'^d/(?P<dedication>\d+)', 'dest': render.single}]

dispatch(path, rules)
