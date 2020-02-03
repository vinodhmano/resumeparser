from app import app, api, db
from app.forms import UploadCandidateForm
from app.models import Candidate
from main import get_skills, process_candidate

from flask import render_template, flash, request, url_for
from flask_restful import Resource, reqparse
from config import Config

import os
import datetime

"""
Rest API call
The resource can be accessed by POST request to the url <servername:port>/get_skills
the POST request should include the body 'application/json' = path of the resume
curl -i -X POST -H 'Content-Type : 'application/json' -d {"resumeurl : "path to the resume"}
"""


# class Candidate(Resource):
#
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument('resumeurl', type=str)
#
#     def post(self):
#         args = self.parser.parse_args()
#         print(args)
#         print(args['resumeurl'])
#
#         candidate = process_candidate(path=args['resumeurl'])
#         return {'email_id': candidate.email_id,
#                 'skills': candidate.skills
#                 }
#
#
# api.add_resource(Candidate, '/api/v1.0/get_skills')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    candidates = []

    target = os.path.join(Config.APP_ROOT, 'temp')
    # print("target folder", target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        # print("file name " , file)
        filename = file.filename
        destination = "\\".join([target, filename])
        # print("destination folder ", destination)
        file.save(destination)

        # skills.extend(get_skills(destination))
        # print(skills)

        # extract email
        candidate = process_candidate(path=destination)
        # print('Canddiate Email ID : {}'.format(candidate.email_id))
        # print('Candidate skills : {}'.format(candidate.skills))
        candidates.append(candidate)
        # TODO : Write code to delete the file from the temp folder
        os.chmod(destination, 0o0777)
        os.remove(destination)

    return render_template('results.html', candidates=candidates)


@app.route('/resume_upload', methods=['GET', 'POST'])
def resume_upload():
    form = UploadCandidateForm()

    # target = os.path.join(Config.APP_ROOT, 'temp')
    # #print("target folder", target)
    #
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    #
    # if form.validate_on_submit():
    #     file = request.files["file"]
    #     filename = file.filename
    #     destination = "\\".join([target,filename])
    #     # print("destination folder ", destination)
    #     file.save(destination)
    #
    #     #skills.extend(get_skills(destination))
    #     #print(skills)
    #
    #     #extract email
    #     candidate = process_candidate(path=destination)
    #
    #     c = Candidate(
    #         firstname = form.firstname.data,
    #         middlename = form.middlename.data,
    #         lastname = form.lastname.data,
    #         email_id = form.email_id.data,
    #         contact_number = form.contact_number.data,
    #         skills = candidate.skills
    #     )

    return render_template('resume_upload.html', form=form)

@app.route('/resume_results',methods=['GET','POST'])
def resume_results():
    candidates = []
    candidates_skills_list = []
    target = os.path.join(Config.APP_ROOT, 'temp')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "\\".join([target,filename])
        file.save(destination)

        candidate = process_candidate(path=destination)
        candidates.append(candidate)

        if candidate.skills.__len__() != 0:
            candidates_skills_list.extend(candidate.skills)

        #TODO : Write code to delete the file from the temp folder
        os.chmod(destination,0o0777)
        os.remove(destination)

        _firstname = request.form['firstname'] or "Unknown"
        _middlename = request.form['middlename'] or "Unknown"
        _lastname = request.form['lastname'] or "Unknown"
        _email_id = request.form['email_id'] or "Unknown"
        _contact_number = request.form['contact_number'] or "Unknown"
        _skills = ','.join(candidates_skills_list) or "No skills found"

        ocandidate = Candidate(firstname = _firstname,
                              middlename = _middlename,
                              lastname = _lastname,
                              email_id = _email_id,
                              contact_number = _contact_number,
                              date_added = datetime.datetime.now(),
                              last_modified = datetime.datetime.now(),
                              skills = _skills
                              )
        print(ocandidate)
        #TODO : Write Code here to insert the candidate into database

    return render_template('results.html', candidates=candidates)

# @app.route('/resume_results',methods=['GET','POST'])
# def resume_results():
#     # skills = ['xml', 'python', 'java']
#     skills = []
#     _firstname = request.form['firstname'] or "Unknown"
#     _middlename = request.form['middlename'] or "Unknown"
#     _lastname = request.form['lastname'] or "Unknown"
#     _email_id = request.form['email_id'] or "Unknown"
#     _contact_number = request.form['contact_number'] or "Unknown"
#     _skills = ','.join(skills) or "No skills found"
#     print (_firstname, _middlename, _lastname, _email_id, _contact_number, _skills)
#     return "Working"