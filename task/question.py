#!/usr/bin/python

import cgitb, cgi, MySQLdb
import cPickle as p
from random import shuffle
from qs import questions,emoanswers, itemlabels
import ndim_funcs as ndf
import config as cf
from config import names,emolist,subjects
#
printpage=cf.htmldict['question']
tablename=cf.table
dimfile=cf.datadict['appraisals']
errorpage=cf.htmldict['errorpage']
#
#get the form from previous page
myform=cgi.FieldStorage()
theids=myform.keys()
subjid = myform['subjid'].value
#
##enable cgi and open the database cursor
cgitb.enable()
print 'Content-type:text/html\n\n'
cursor = MySQLdb.connect(host=cf.host,user=cf.user,passwd=cf.passwd,db=cf.db).cursor()

#get the appraisal dimension info
[minindex,midindex,maxindex,Qindex,qlabelindex,qnumindex,dimdata,numdims]=ndf.extractdims(dimfile)

match=0
#determine if the subject provided a reasonable subject ID, and which question they have been assigned
if subjid in subjects: 
    subjindex=subjects.index(subjid)
    match=1
else: 
    match=0
if match==0: #if not a match, print the error page

    newhtml=ndf.gethtml(errorpage)
    head=ndf.gethtml(cf.htmldict['head'])
    newhtml=newhtml.replace('head_var', head)
    print newhtml
else: #if a match, print the good stuff
    possqs = myform['possqs'].value
    try:
        possqs = ndf.string2intlist(possqs)
        shuffle(possqs)
    except:#will fail when number of rounds is maxe
        pass
    thisround=int(myform['thisround'].value)
    if thisround==1: #for first round, question dictated by ID
        questionID=ndf.defineQ(subjid)
        qnum=int(questionID)
    else: #after that, pull from remaining list
        qnum=int(myform['qnum'].value)
    try:
        myqnums=possqs.remove(qnum)
    except:
        pass
    dnums=list(eval(myform['dnums'].value))
    totalqpersubj=len(dnums)
    qindex=myform['qindex'].value
    qindex=int(qindex)+1
    if qindex==1:
        formindex=ndf.enteruser(cursor,subjid,tablename)
        nextthing='question.py'
    elif qindex<totalqpersubj:
        formindex=ndf.savelastentry(cursor, tablename, myform, emolist)
        nextthing='question.py'
    elif qindex==totalqpersubj:
        formindex=ndf.savelastentry(cursor, tablename, myform, emolist)
        nextthing='roundup.py'   
        #print "main loop"
    elif qindex>totalqpersubj:
        nextthing='question.py'
        qindex=1
        thisround=thisround+1
        qnum=int(possqs[0])
        formindex=ndf.enteruser(cursor,subjid,tablename)
        shuffle(dnums)
    dnum=dnums[qindex-1]
    thisdim=dimdata[dnum-1]
    mintag=thisdim[minindex]
    midtag=thisdim[midindex]
    maxtag=thisdim[maxindex]
    dlabel=thisdim[qlabelindex]
    dquest=thisdim[Qindex]
    question=questions[qnum]
    emoans=emoanswers[qnum]
    qname=names[qnum]
    dquest=dquest.replace('NAMEVAR', qname)
    itemlabel=itemlabels[qnum]
    question=question.replace('NAMEVAR', qname)
    
    newhtml=ndf.gethtml(printpage)
    emoquest='How did NAMEVAR feel in this situation?'
    emoquest=emoquest.replace('NAMEVAR',qname)
    if dquest!=emoquest:
        printblock=ndf.make_scale(mintag,midtag,maxtag,cf.htmldict['slider'])
    else:
        printblock=ndf.make_scaleseries(emolist)
        #printblock=ndf.make_checkarray(emolist)
    newhtml=newhtml.replace('printblock_var', printblock)
    newhtml=newhtml.replace('qnum_var',str(qnum))
    newhtml=newhtml.replace('qindex_var',str(qindex))
    newhtml=newhtml.replace('totalqpersubj_var',str(totalqpersubj))
    newhtml=newhtml.replace('question_var',question)
    newhtml=newhtml.replace('dquest_var',dquest)
    newhtml=newhtml.replace('nextthing_var',nextthing)
    newhtml=newhtml.replace('subjid_var',subjid)
    newhtml=newhtml.replace('itemlabel_var',itemlabel)
    newhtml=newhtml.replace('emoans_var',emoans)
    newhtml=newhtml.replace('dnumlist_var',str(dnums))
    newhtml=newhtml.replace('formindex_var',formindex)
    newhtml=newhtml.replace('dlabel_var',dlabel)
    newhtml=newhtml.replace('possqs_var',str(possqs))
    newhtml=newhtml.replace('thisround_var',str(thisround))
    head=ndf.gethtml(cf.htmldict['head'])
    newhtml=newhtml.replace('head_var', head)
    
    print newhtml

    
