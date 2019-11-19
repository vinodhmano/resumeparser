from app import app, api
from flask import render_template, flash, request, url_for
from flask_restful import Resource, reqparse
from config import Config
from main import get_skills, Candidate, process_candidate
import os


"""
Rest API call
The resource can be accessed by POST request to the url <servername:port>/get_skills
the POST request should include the body 'application/json' = path of the resume
curl -i -X POST -H 'Content-Type : 'application/json' -d {"resumeurl : "path to the resume"}
"""

class Candidate(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('resumeurl',type=str)

    def post(self):
        args = self.parser.parse_args()
        print(args)
        print(args['resumeurl'])
        
        candidate = process_candidate(path=args['resumeurl'])
        return { 'email_id' : candidate.email_id,
                 'skills' : candidate.skills
               }

api.add_resource(Candidate,'/api/v1.0/get_skills')

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/results',methods=['GET','POST'])
def results():
    candidates = []
   
    target = os.path.join(Config.APP_ROOT, 'temp')
    #print("target folder", target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):

        #print("file name " , file)
        filename = file.filename
        destination = "\\".join([target,filename])
        # print("destination folder ", destination)
        file.save(destination)
        
        #skills.extend(get_skills(destination))
        #print(skills)

        #extract email
        candidate = process_candidate(path=destination)
        # print('Canddiate Email ID : {}'.format(candidate.email_id))
        # print('Candidate skills : {}'.format(candidate.skills))
        candidates.append(candidate)
        #TODO : Write code to delete the file from the temp folder
        os.chmod(destination,0o0777)
        os.remove(destination)

    
    return render_template('results.html', candidates=candidates)