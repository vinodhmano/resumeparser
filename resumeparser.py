from app import app
from app.models import Candidate
from app import db

@app.shell_context_processor
def make_shell_processor():
    return {'db': db, 'Candidate' : Candidate}

if __name__ == '__main__':
    app.run(port=5000, debug=False)