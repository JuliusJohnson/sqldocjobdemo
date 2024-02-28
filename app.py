import csv,dbConnection
from flask import Flask, render_template, render_template_string, abort
from pprint import pprint
# declaring app name 
app = Flask(__name__) 

def getJobStepData(jobName):
    getJobStepData = dbConnection.getJobs(jobName)
    return getJobStepData

def structureData():
    keys = []
    columns = []
    jobs = {}

    for job in getJobStepData(''):
        keys.append(job[0])

    for column in getJobStepData('').description:
        columns.append(column[0])

    keys = list(set((keys))) #makes unique list

    for key in keys: #for each key in the keys list
        jobs[key] = [] #create a dictionary entry with an empty list
        for i in getJobStepData('').fetchall(): #for each "row" from the query while looping through keys
            if i[0] == key: #if the jobname is equal to the key name
                jobs[key].append(dict(zip(columns,i))) #append that row to the corresponding key name. Help: https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary
        
    return jobs

pprint(structureData()['Long Job'][0]['step_name'])

# defining home page 
@app.route(f'/') 
def homepage(): 
  
# returning index.html and list 
# and length of list to html page 
    return render_template("index.html", len = len(structureData()['Long Job']), jobSteps = structureData()['Long Job']) 

# @app.route('/<string:title>')
# def post(number):
#     if number < 1 or number > len(select_jobsteps('t')):
#         abort(404, "This Post doesn't exist")   

#     data = select_jobsteps('t')[number-1]
    
#     return render_template_string('''
# {{ item[0]['JobName'] }}<br/>
# {{ item.content }}<br/>
# {{ item.date }}<br/>
# {{ item.author }}<br/>''', item=select_jobsteps('t')) 
# if __name__ == '__main__': 
  
# running app 
app.run(use_reloader = True, debug = True) 


