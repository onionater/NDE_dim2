import csv

###all hardcoded variables here
#filenames
htmldict={'head':'html/head.html','login':'html/login.html', 'question':'html/question.html', 'roundup':'html/roundup.html', 'summary':'html/summary.html', 'demographics':'html/demographics.html', 'keycode':'html/keycode.html', 'errorpage':'html/iderror.html', 'slider':'html/slider.html'}
datadict={'config':'appdata/config_data.csv', 'stimfile':'appdata/NDE_stims.csv', 'subjectfile':'appdata/slist.csv', 'appraisals':'appdata/appraisals.csv'}
#mysql info
table='NDE_dims2'
host="localhost"
user="askerry"
passwd="password"
db="aesbehave"
#variables
baserate=.30
rate=.30

####

def getdata(configfile, string1, string2):
    with open(configfile, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for subjnum, row in enumerate(reader):
            if subjnum==0:
                colnames=row
                reader = csv.reader(csvfile)
                rowdata=list(reader) 
                coldata=zip(*rowdata) #handytranspose
                s1index=colnames.index(string1)
                s2index=colnames.index(string2)
                s1=coldata[s1index]
                s2=coldata[s2index]
                thing1=[t1 for t1 in s1 if t1 !='']
                thing2=[t2 for t2 in s2 if t2 !='']
    return thing1, thing2
    
[emolist, names]=getdata(datadict['config'], 'emotionlist', 'names')
[subjects, keycodes]=getdata(datadict['subjectfile'], 'subjects', 'keycodes')