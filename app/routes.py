from app import app
from flask import render_template, flash, request, url_for
from app.forms import BrowsingForm
from config import Config
from main import get_skills
import os

@app.route('/')
def index():
    return render_template("upload.html")

@app.route('/upload',methods=['GET','POST'])
def upload():
    skills = []
    target = os.path.join(Config.APP_ROOT, 'temp')
    print("target folder", target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print("file name " , file)
        filename = file.filename
        destination = "\\".join([target,filename])
        print("destination folder ", destination)
        file.save(destination)
        skills.extend(get_skills(destination))
        print(skills)
    return render_template('completed.html', skills=skills)