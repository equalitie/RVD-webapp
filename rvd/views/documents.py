from flask import Blueprint, render_template
from flask_login import login_required
documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/document/add', methods=('GET', 'POST'))
@login_required
def documents_add():
    return render_template("document_add.html")