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
    uploaded_files = request.files.getlist("file[]")

    if uploaded_files:
        for file in uploaded_files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                f = os.path.join(UPLOAD_FOLDER, filename)
                #org_name = request.form['organisation_name']
                #print '### Got organisation name ' + org_name
                user_id = current_user.id
                user = rvd.models.session.query(rvd.models.User).filter_by(id=user_id).first()
                parsed_docx = False
                if user.organisation_id is not None:
                    org = rvd.models.session.query(rvd.models.Organisation).filter_by(
                        id=user.organisation_id).first()
                    if org is not None and filename.split('.')[-1].lower() == 'docx':
                        if 'ccdhrn' in org.name.lower():
                            print '### Parsing org1\'s docx file'
                            try: parsers.parse(f, parsers.ORG1_DOCX)
                            except Exception as ex:
                                print '!!! Failed to parse org1 docx' 
                                print ex.message
                            else: parsed_docx = True
                        elif 'cihpress' in org.name.lower():
                            print '### Parsing org2\'s docx file'
                            try: parsers.parse(f, parsers.ORG2_DOCX)
                            except Exception as ex:
                                print '!!! Failed to parse org2 docx'
                                print ex.message
                            else: parsed_docx = True
                if not parsed_docx:
                    try: parsers.parse(f, parsers.EXCEL_DOC) #org_name)
                    except Exception as ex:
                        print '!!! Failed to parse file provided.'
                        print ex.message
    return render_template("document_add.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def only_supplies_event(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in EVENT_ONLY
