from flask import Blueprint, render_template
from flask_login import login_required
reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports')
@login_required
def reports():
    return render_template("reports.html")