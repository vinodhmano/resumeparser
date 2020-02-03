from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, StringField
from wtforms.validators import DataRequired


class UploadCandidateForm(FlaskForm):
    # firstname = TextField('First Name')
    firstname = StringField('First Name')
    middlename = StringField('Middle Name')
    lastname = StringField('Last Name')
    email_id = StringField('Email ID')
    contact_number = StringField('Contact Number')
    file = FileField('Resume URL', validators=([DataRequired]))
    submit = SubmitField('Save')
