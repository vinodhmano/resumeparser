from app import app, api
from flask import render_template, flash, request, url_for
from flask_restful import Resource
from config import Config
from main import get_skills, Candidate, process_candidate
import os

# class Index(Resource):
#     def get(self):
#         return render_template("upload.html")

# class Upload(Resource):
#     def get(self):
#         skills = []
#         target = os.path.join(Config.APP_ROOT, 'temp')
#         print("target folder", target)

#         if not os.path.isdir(target):
#             os.mkdir(target)

#         for file in request.files.getlist("file"):
#             print("file name " , file)
#             filename = file.filename
#             destination = "\\".join([target,filename])
#             print("destination folder ", destination)
#             file.save(destination)
#             skills.extend(get_skills(destination))
#             print(skills)

#         return render_template('completed.html', skills=skills)


# api.add_resource(Index,'/')
# api.add_resource(Upload,'/upload')



@app.route('/')
def index():
    return render_template("upload.html")

@app.route('/upload',methods=['GET','POST'])
def upload():
    candidates = []
    skills = []
    target = os.path.join(Config.APP_ROOT, 'temp')
    print("target folder", target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        '''TODO : Write logic to separte the skills per file
                  Right now. It combines all the skills into 1 list while showing
        '''

        print("file name " , file)
        filename = file.filename
        destination = "\\".join([target,filename])
        print("destination folder ", destination)
        file.save(destination)
        
        #skills.extend(get_skills(destination))
        #print(skills)

        #extract email
        candidate = process_candidate(path=destination)
        print('Canddiate Email ID : {}'.format(candidate.email_id))
        print('Candidate skills : {}'.format(candidate.skills))
        candidates.append(candidate)
        #TODO : Write code to delete the file from the temp folder

    return render_template('completed.html', skills=skills, candidates=candidates)