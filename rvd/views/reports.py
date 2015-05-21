from flask import Blueprint, render_template
from flask_login import login_required
from rvd.forms import event_type_factory, location_factory
reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports')
@login_required
def reports():
    event_types_names = [{"id": x.id, "name": x.name} for x in event_type_factory()]
    locations = [{"id": x.id, "name": x.name} for x in location_factory()]

    return render_template("reports.html", rights_violation_types=event_types_names, locations=locations)