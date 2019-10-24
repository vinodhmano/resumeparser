from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, FileField

class BrowsingForm(FlaskForm):
    filename = FileField('Browse')
    submit = SubmitField('Get Skills')