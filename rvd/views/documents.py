from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug import secure_filename

documents_bp = Blueprint('documents', __name__)


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['docx', 'doc', 'xlsx', 'xls'])

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
    return render_template("document_add.html", 'success')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

