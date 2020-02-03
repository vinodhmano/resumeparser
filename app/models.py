from app import db

class Candidate(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(128),index=True)
    middlename = db.Column(db.String(64))
    lastname = db.Column(db.String(128),index=True)
    email_id = db.Column(db.String(160),index=True)
    contact_number = db.Column(db.String(20))
    date_added = db.Column(db.Date)
    last_modified = db.Column(db.Date)
    skills = db.Column(db.Text)

    def __repr__(self):
        return 'Candidate id: {} | email_id : {} | skills : {}' \
               ' | date_added : {} | date_modified : {}'.format(self.id, self.email_id, self.skills, self.date_added, self.last_modified)