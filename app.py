import csv
from flask import Flask, render_template 

# declaring app name 
app = Flask(__name__) 

def read_data():
    with open('testjobdata.csv', mode = 'r') as jobsData:
        dictJobsData = list(csv.DictReader(jobsData))
        return dictJobsData
    #listofDict = list(dict_reader)

def get_jobnames():
    jobNames = []
    jobsData = read_data()
    for job in jobsData:
        jobNames.append(job['JobName'])   
    uniqueJobNames = list(dict.fromkeys(jobNames))
    return uniqueJobNames

def select_jobsteps(job):
    jobSteps = []
    for i in read_data():
        if i['JobName'] == str(job):
            jobSteps.append(i)
    return jobSteps

# defining home page 
@app.route('/') 
def homepage(): 
  
# returning index.html and list 
# and length of list to html page 
    return render_template("index.html", len = len(select_jobsteps('Test1')), jobSteps = select_jobsteps('Test1')) 
  
# if __name__ == '__main__': 
  
# running app 
app.run(use_reloader = True, debug = True) 


