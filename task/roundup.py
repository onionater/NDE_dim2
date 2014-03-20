#!/usr/bin/python

import cgitb, cgi, MySQLdb
from qs import questions
import ndim_funcs as ndf
import config as cf
from config import emolist
#
printpage=cf.htmldict['roundup']
tablename=cf.table
##
myform=cgi.FieldStorage()
cgitb.enable()
print 'Content-type:text/html\n\n'
cursor = MySQLdb.connect(host=cf.host,user=cf.user,passwd=cf.passwd,db=cf.db).cursor()


theids=myform.keys() 
subjid = myform['subjid'].value
questionID=ndf.defineQ(subjid)
qnum=int(questionID)
qindex=myform['qindex'].value
possqs = myform['possqs'].value
try:
    possqs = ndf.string2intlist(possqs)
except:
    pass #will fail when number of rounds is maxe
dnums=list(eval(myform['dnums'].value))
thisround=int(myform['thisround'].value) 
formindex=ndf.savelastentry(cursor, tablename, myform, emolist)
possrounds=len(questions)
if thisround==1:
    thisroundunit='round'
else:
    thisroundunit='rounds'
if thisround==possrounds:
    printpage=cf.htmldict['summary']
totalpayment=cf.baserate+cf.rate*(int(thisround)-1)

#print the page
newhtml=ndf.gethtml(printpage)
newhtml=newhtml.replace('qindex_var',str(qindex))
newhtml=newhtml.replace('qnum_var',str(qnum))
newhtml=newhtml.replace('nextthing_var','demographics.py')
newhtml=newhtml.replace('subjid_var',subjid)
newhtml=newhtml.replace('dnumlist_var',str(dnums))
newhtml=newhtml.replace('formindex_var',str(formindex))
newhtml=newhtml.replace('possqs_var',str(possqs))
newhtml=newhtml.replace('thisround_var',str(thisround))
newhtml=newhtml.replace('thisroundunit_var',thisroundunit)
newhtml=newhtml.replace('possrounds_var',str(possrounds))
newhtml=newhtml.replace('rate_var', str(cf.rate))
newhtml=newhtml.replace('totalpayment_var', str(totalpayment))
head=ndf.gethtml(cf.htmldict['head'])
newhtml=newhtml.replace('head_var', head)

print newhtml
