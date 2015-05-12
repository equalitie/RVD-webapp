from flask import Blueprint, render_template, request
import rvd.models
from werkzeug.utils import secure_filename
import os
from flask_login import login_required
from rvd import parsers

documents_bp = Blueprint('documents', __name__)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['docx', 'doc', 'xlsx', 'xls'])

# Document types that only provide information about events.
EVENT_ONLY = set(['docx', 'doc'])

@documents_bp.route('/document/add', methods=('GET', 'POST'))
@login_required
def documents_add():
    return render_template("document_add.html")

@documents_bp.route('/document/upload', methods=('POST',))
@login_required
def documents_uploads():
    print '### In documents_uploads()'
    uploaded_files = request.files.getlist("file[]")

    print '### Got uploaded files ' + str(uploaded_files)
    if uploaded_files:
        for file in uploaded_files:
            print '### Found file ' + file.filename
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print '### Trying to save ' + filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                print '### Saved'
                f = os.path.join(UPLOAD_FOLDER, filename)
                #org_name = request.form['organisation_name']
                #print '### Got organisation name ' + org_name
                parsed = parsers.parse(f, parsers.EXCEL_DOC) #org_name)
                print '### Succeeding in parsing document'
                if 'error' in parsed:
                    print '### ' + parsed['error']
                    return render_template('document_add.html')
                elif only_supplies_event(file.filename):
                    rvd.models.session.add_all(parsed['events'])
                    print '### Added all parsed events'
                else:
                    # !!!! TODO !!!!
                    # Pull the owner id out of the flask session and find the actual user instance.
                    admin = rvd.models.session.query(rvd.models.User).first()
                    for i in range(len(parsed[parsers.ACTORS])):
                        parsed[parsers.ACTORS][i].owner_id = 0
                        parsed[parsers.ACTORS][i].owner = admin
                    for i in range(len(parsed[parsers.EVENTS])):
                        parsed[parsers.EVENTS][i].owner_id = 0
                        parsed[parsers.EVENTS][i].owner = admin
                    for entity in parsed:
                        rvd.models.session.add_all(parsed[entity])
                        
                    print '### Added all parsed entities'
                rvd.models.session.commit()
                        
    return render_template("document_add.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def only_supplies_event(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in EVENT_ONLY
