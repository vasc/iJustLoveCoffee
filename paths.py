#! /usr/bin/python
 
#routes like dispatcher to work on plain cgi
#request url looks like this 'paths.py?path=/abc/def/ghj/;' after mod_rewrite
 
import re
import cgi
import cgitb
import render

cgitb.enable() 

def dispatch(path, rules, vars):
    for rule in rules:
        dest = rule['dest']
        r = re.search(rule['re'], path)
        if(r):
            vars.update(r.groupdict())
            try:
                dest(**vars)
            except TypeError:
                render.page_404()
            return
    render.page_404()
 
 

form = cgi.FieldStorage()
path = ''
if 'path' in form:
    path = form['path'].value

vars = {}
for var in form:
    if var != 'path':
        vars[var] = form[var].value


rules = [ {'re': r'^$', 'dest': render.main},
          {'re': r'^page/(?P<page>\d+)', 'dest': render.main},
          {'re': r'^d/(?P<d_id>\d+)', 'dest': render.single},
          {'re': r'^feed', 'dest': render.feed},
          {'re': r'^add-dedication', 'dest': render.add_dedication},
          {'re': r'^delete/(?P<id>\d+)/(?P<secret>\d+)', 'dest': render.del_dedication}]

dispatch(path, rules, vars)
#render.send_html(vars)

