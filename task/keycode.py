#!/usr/bin/python

#import the modules we need to run the script
import cgitb, cgi, MySQLdb
import ndim_funcs as ndf
import config as cf
from config import subjects, keycodes

printpage=cf.htmldict['keycode']
tablename=cf.table

myform=cgi.FieldStorage()
cgitb.enable()
print 'Content-type:text/html\n\n'
cursor = MySQLdb.connect(host=cf.host,user=cf.user,passwd=cf.passwd,db=cf.db).cursor()

subjid = myform['subjid'].value
subjindex=subjects.index(subjid)
keycode=keycodes[subjindex]
thisround = myform['thisround'].value
if int(thisround)==1:
    thisroundunit='round'
else:
    thisroundunit='rounds'
totalpayment=cf.baserate+cf.rate*(int(thisround)-1)

#add the person to the database:  "insert" command for new rows
ndf.savedemodata(cursor, tablename, myform)

#print the page
newhtml=ndf.gethtml(printpage)
newhtml=newhtml.replace('keycode_var', keycode) 
newhtml=newhtml.replace('totalrounds_var', str(thisround))
newhtml=newhtml.replace('totalpayment_var', str(totalpayment))
newhtml=newhtml.replace('thisroundunit_var',thisroundunit)
head=ndf.gethtml(cf.htmldict['head'])
newhtml=newhtml.replace('head_var', head)

print newhtml

