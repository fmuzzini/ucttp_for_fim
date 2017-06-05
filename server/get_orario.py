#!python

f = open("orario.json", "r")

print "Content-type: application/json"
print ""

print f.read()