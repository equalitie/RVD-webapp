from flask import Blueprint, render_template, request
from flask_login import current_user
import rvd.models
from werkzeug.utils import secure_filename
import os
from flask_login import login_required
from rvd import parsers

documents_bp = Blueprint('documents', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'doc', 'xlsx', 'xls'}

# Document types that only provide information about events.
EVENT_ONLY = {'docx', 'doc'}


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
                parsers.parse(f, parsers.EXCEL_DOC) #org_name)
                print '### Succeeded in parsing document'
                #user_id = current_user.id
                #user = rvd.models.session.query(rvd.models.User).filter_by(id=user_id).first()
    return render_template("document_add.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def only_supplies_event(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in EVENT_ONLY
