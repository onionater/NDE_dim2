import csv
import math
import datetime

def extractdims(dimfile):
    with open(dimfile, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        dimdata=[]
        for dimnum, row in enumerate(reader):
            if dimnum==0:
                minindex=row.index('LowEnd')
                midindex=row.index('Middle')
                maxindex=row.index('HighEnd')
                Qindex=row.index('Dquestion')
                qlabelindex=row.index('Dqname')
                qnumindex=row.index('Dnum')
            else:
                dimdata.append(row)
        numdims=len(dimdata)
    return minindex,midindex,maxindex,Qindex,qlabelindex,qnumindex,dimdata,numdims  

#[minindex,midindex,maxindex,Qindex,qlabelindex,qnumindex,dimdata,numdims]=extractdims(dimfile) 

def gethtml(filename):
    with open(filename, "r") as myfile: 
        newhtml=myfile.read().replace('\n', '') 
    return newhtml

def enteruser(cursor,subjid,tablename):
    #add the person to the database:  "insert" command for new rows
    sql='insert into %s (subjid) values ("%s")'%(tablename, str(subjid))
    cursor.execute(sql)
    sql='SELECT MAX(rownum) AS formindex FROM %s' %(tablename)
    formindex=cursor.execute(sql)
    formindex = cursor.fetchone()
    thisvar=str(formindex)
    thisvar=thisvar[1:-3]
    return thisvar
    
def savedata(cursor, tablename, column, value, row):
    sql='update '+tablename+' set ' +column +' ="'+value+'" where rownum="'+row+'"'
    #print sql
    cursor.execute(sql)
    
def savedemodata(cursor, tablename, form):
    age = form['age'].value
    gender = form['gender'].value
    formindex=form['rownum'].value
    response_noface=form['response_noface'].value
    response_nothought=form['response_nothought'].value
    response_needverbal=form['response_needverbal'].value
    response_facevoice=form['response_facevoice'].value
    response_surprised=form['response_surprised'].value
    datevar=datetime.datetime.now()
    datevar=datevar.strftime("%Y-%m-%d %H:%M")
    # store data onto server:  "update" commands to add data to existing row
    savedata(cursor,tablename,'age',age,formindex)
    savedata(cursor,tablename,'gender',gender,formindex)
    savedata(cursor,tablename,'submission_date',datevar,formindex)
    for x in ['country','city','thoughts']:
        try:
            it = form[x].value
            savedata(cursor,tablename,x,it,formindex)
        except:
            pass
    savedata(cursor,tablename,'response_noface',response_noface,formindex)
    savedata(cursor,tablename,'response_nothought',response_nothought,formindex)
    savedata(cursor,tablename,'response_needverbal',response_needverbal,formindex)
    savedata(cursor,tablename,'response_facevoice',response_facevoice,formindex)
    savedata(cursor,tablename,'response_surprised',response_surprised,formindex)

def savelastentry(cursor, tablename, myform, emolist):
    formindex=myform['rownum'].value
    lastitem=myform['item'].value
    qvardim=myform['dlabel'].value
    lastanswer=myform['correctans'].value
    qvaremo=qvardim+'_qemo'
    qvaritem=qvardim+'_qlabel'
    try:
        lastresponse=myform['response'].value
        savedata(cursor,tablename,qvardim,lastresponse,formindex)
        savedata(cursor,tablename,qvaremo,lastanswer,formindex)
        savedata(cursor,tablename,qvaritem,lastitem,formindex)
    except:
        for emo in emolist:
           emoresp=myform[emo].value
           savedata(cursor,tablename,emo+'_extent',emoresp,formindex)
           savedata(cursor,tablename,qvardim,lastanswer,formindex)
    return formindex

def make_checkarray(emolist):
    numemos=len(emolist)
    #numcols=math.floor(math.sqrt(numemos))
    if numemos<4:
        numcols=numemos
    else:
        numcols=math.floor(math.sqrt(len(emolist)))
    numcols=4 #this will be prettier for this one
    buckets=[[] for i in range(0,numcols)]
    for n, emo in enumerate(emolist):
        col=int(n%numcols)
        if n==0:
            emostring='<input type="radio" name="response" value="%s" checked><label for="%s">%s</label>' % (emo,emo,emo)
        else:
		emostring='<input type="radio" name="response" value="%s"><label for="%s">%s</label>' % (emo,emo,emo)
		buckets[col].append(emostring)
  
    buckets[-1].append('<input type="radio" name="response" value="neutral" checked><label for="neutral">Neutral</label>')
    printblock=''
    for c in buckets:
        printblock=printblock+'<div>'
        for e in c:
		printblock=printblock+ e
        printblock=printblock+'</div>'
    return printblock
def make_scaleseries(emolist):
    printblock='<div><p>Rate the extent to which the target is feeling each emotion.</p>'
    for emo in emolist:
        printblock=printblock+'<div><span><b>%s: </b></span><span class="emoslider">not at all<input type="range" name="%s" value="5" min="0" max="10" step="1" id="%s"/>very strongly</span></div>' % (emo,emo,emo)
    printblock=printblock+'<div><span><b>Neutral: </b></span><span class="emoslider">not at all<input type="range" name="Neutral" value="5" min="0" max="10" step="1" id="Neutral"/>very strongly</span></div></div>'
    return printblock
def make_scale(mintag,midtag,maxtag, html):
    printblock=gethtml(html)
    printblock=printblock.replace('mintag_var',mintag)
    printblock=printblock.replace('midtag_var',midtag)
    printblock=printblock.replace('maxtag_var',maxtag)
    return printblock
    
def defineQ(subjid):
    questionID=subjid[subjid.index('q')+1:subjid.index('q')+3]
    return questionID

def string2intlist(string):
    string = string[1:-1]
    mylist=[int(x) for x in string.split(',')]
    return mylist
    