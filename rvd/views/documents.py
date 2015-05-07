from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug import secure_filename
from ....lib import parsers
from ..models import *

documents_bp = Blueprint('documents', __name__)


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['docx', 'doc', 'xlsx', 'xls'])

# Document types that only provide information about events.
EVENT_ONLY = set(['docx', 'doc'])

@documents_bp.route('/document/add', methods=('GET', 'POST'))
@login_required
def documents_add():
    return render_template("document_add.html")

@documents_bp.route('/document/upload', methods=('POST'))
@login_required
def documents_uploads():
    uploaded_files = flask.request.files.getlist("file[]") 

    if uploaded_files:
        for file in uploaded_files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                f = os.path.join(UPLOAD_FOLDER, filename)
                org_name = flask.request.form['organisation_name']
                print 'Got organisation name ' + org_name
                parsed = parsers.parse(f, org_name)
                if 'error' in parsed:
                    print parsed['error']
                    return render_template('document_add.html', 'failure')
                elif only_supplies_event(file.filename):
                    session.add_all(parsed['events'])
                else:
                    for entity in parsed:
                        session.add_all(parsed[entity])
                session.commit()
                        
    return render_template("document_add.html", 'success')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def only_supplies_event(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in EVENT_ONLY
