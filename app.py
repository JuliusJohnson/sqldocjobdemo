import csv,dbConnection, datetime
from flask import Flask, render_template, render_template_string, abort
from pprint import pprint
# declaring app name 
app = Flask(__name__) 
today = datetime.datetime.now().strftime("%B %d, %Y %I:%M %p")

def getJobStepData(jobName):
    getJobStepData = dbConnection.getJobs(jobName)
    return getJobStepData

def structureData():
    keys = []
    columns = []
    jobs = {}

    for job in getJobStepData('%'):
        keys.append(job[0])

    for column in getJobStepData('%').description:
        columns.append(column[0])

    keys = list(set((keys))) #makes unique list

    for key in keys: #for each key in the keys list
        jobs[key] = [] #create a dictionary entry with an empty list
        for i in getJobStepData('%').fetchall(): #for each "row" from the query while looping through keys
            if i[0] == key: #if the jobname is equal to the key name
                jobs[key].append(dict(zip(columns,i))) #append that row to the corresponding key name. Help: https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary
        
    return jobs

# pprint(getJobStepData('%').fetchall())

# defining home page 
@app.route(f'/') 
def homepage(): 
  
# returning index.html and list 
# and length of list to html page 
    return render_template("index.html", len = len(structureData()), jobSteps = [structureData()]) 

@app.route('/jobs/<jobname>')
def jobSteps(jobname):
    return render_template("jobs.html", len = len(structureData()[jobname]), jobSteps = structureData()[jobname], getdate = today)
  
# running app 
app.run(use_reloader = True, debug = True) 


