from app import app
from flask import render_template, flash, request, url_for
from app.forms import BrowsingForm
from config import Config
from try2_list_lookup import get_skills_2
import os

@app.route('/')
def index():
    return render_template("upload.html")

@app.route('/upload',methods=['GET','POST'])
def upload():
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
        skills = get_skills_2(destination)
        print(skills)
    return render_template('completed.html', skills=skills)