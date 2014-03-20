#!/usr/bin/python

import cgitb, cgi
from random import shuffle
from qs import possqs
import ndim_funcs as ndf
import config as cf

#variable definition
dimfile=cf.datadict['appraisals']
printpage=cf.htmldict['login']

myform=cgi.FieldStorage()
cgitb.enable()
print 'Content-type:text/html\n\n'

theids=myform.keys()
qindex=myform['qindex'].value

#figure out the dimensions you'll be asking about
[minindex,midindex,maxindex,Qindex,qlabelindex,qnumindex,dimdata,numdims]=ndf.extractdims(dimfile)
dnums=[]
for dim in dimdata:
    dnums.append(dim[qnumindex])
shuffle(dnums)
dnumlist=reduce(lambda x,y:x+','+y, dnums)

#print the page
newhtml=ndf.gethtml(printpage)
newhtml=newhtml.replace('qindex_var',str(qindex))
newhtml=newhtml.replace('dnumlist_var',str(dnumlist))
newhtml=newhtml.replace('nextthing_var','question.py')
newhtml=newhtml.replace('possqs_var',str(possqs))
head=ndf.gethtml(cf.htmldict['head'])
newhtml=newhtml.replace('head_var', head)

print newhtml 


