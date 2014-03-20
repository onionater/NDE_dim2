import csv
import config as cf

stimfile=cf.datadict['stimfile']

def getquestions(stimfile):
    questions=[]
    itemlabels=[]
    emoanswers=[]
    with open(stimfile, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        count=0
        for subjnum, row in enumerate(reader):
            if subjnum==0:
                colnames=row
                print 'varnames in csv: '+str(colnames)
                questionindex=colnames.index('cause')
                emoanswerindex=colnames.index('emotion')
                incindex=colnames.index('keeper')
            else:
                subjdata=row
                if int(subjdata[incindex]):
                    quest=subjdata[questionindex]
                    #print quest
                    quest=quest.replace("!!!","\'" )
                    questions.append(quest)
                    count=count+1
                    itemlabels.append('q'+str(count))
                    emoanswers.append(subjdata[emoanswerindex])
    return questions, itemlabels, emoanswers
                    
[questions, itemlabels, emoanswers]=getquestions(stimfile)
possqs=range(0,len(questions))
