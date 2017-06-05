#!python

import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
orario = form.getfirst('item_to_save')
back = form.getfirst('item_back')
try:
    file = form.getfirst('file')
except:
    file = None

f = open("orario.json", "w")
f.write(orario)

if not file:
    print "Status: 204"
    print ""
    exit(0)

print "Content-Disposition: attachment; filename=orario.json"
print "Content-type: application/json"
print ""

print back