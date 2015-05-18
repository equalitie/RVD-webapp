from flask import Blueprint, render_template
from flask_login import login_required
from rvd.forms import rights_violations_factory, location_factory
reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports')
@login_required
def reports():
    rights_violations_names = [{"id": x.id, "name": x.name} for x in rights_violations_factory()]
    locations = [{"id": x.id, "name": x.name} for x in location_factory()]

    return render_template("reports.html", rights_violation_types=rights_violations_names, locations=locations)