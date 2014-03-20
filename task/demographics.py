#!/usr/bin/python

import cgitb, cgi, MySQLdb, ast
#import cgitb, cgi, ast
import ndim_funcs as ndf
import config as cf

printpage=cf.htmldict['demographics']
tablename=cf.table

myform=cgi.FieldStorage()
cgitb.enable()
print 'Content-type:text/html\n\n'
cursor = MySQLdb.connect(host=cf.host,user=cf.user,passwd=cf.passwd,db=cf.db).cursor()

subjid = myform['subjid'].value
formindex=myform['rownum'].value 
thisround=int(myform['thisround'].value)

#print the page
newhtml=ndf.gethtml(printpage)
newhtml=newhtml.replace('subjid_var',str(subjid))
newhtml=newhtml.replace('formindex_var',str(formindex))
newhtml=newhtml.replace('nextthing_var','keycode.py')
newhtml=newhtml.replace('thisround_var',str(thisround))
head=ndf.gethtml(cf.htmldict['head'])
newhtml=newhtml.replace('head_var', head)

print newhtml
