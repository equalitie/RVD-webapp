from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.RightsViolation import RightsViolationForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session
from rvd.models import RightsViolation
from copy import copy
names = {
    'name': 'rights violation',
    'plural': 'rights violations',
    'slug': 'rights_violation',
    'plural_slug': 'rights_violations'
}
rights_violations_bp = Blueprint('rights_violations', __name__)


def get_name_from_id(needle, things):
    for thing in things:
        if int(thing.id) == int(needle):
            return thing


def gather_form_data():
    rights_violation_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    rights_violation_instance = RightsViolation(**rights_violation_dict)
    session.add(rights_violation_instance)
    session.commit()

    return rights_violation_instance


@rights_violations_bp.route('/rights_violations/add', methods=('GET', 'POST'))
@login_required
def rights_violations():
    rights_violation_form = RightsViolationForm(request.form)
    if helpers.validate_form_on_submit(rights_violation_form):
        rights_violation_instance = gather_form_data()
        return redirect('/rights_violations/{}?success=1'.format(rights_violation_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=rights_violation_form, action='add', data=data)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    from sqlalchemy.inspection import inspect

    for r in inspect(RightsViolation).relationships:
        associated_data = getattr(obj, r.key)
        fields[r.key] = ", ".join([a.name for a in associated_data]) if associated_data else None
    return fields


@rights_violations_bp.route('/rights_violations/<int:rights_violation_id>')
@login_required
def view_rights_violation(rights_violation_id):
    rights_violation = session.query(RightsViolation).get(rights_violation_id)
    fields = flatten_instance(rights_violation)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@rights_violations_bp.route('/rights_violations/all')
@login_required
def view_all_rights_violations():
    all_rights_violations = session.query(RightsViolation).all()
    all_rights_violations = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_rights_violations]

    data = copy(names)
    data['data'] = all_rights_violations

    return render_template("item_view_all.html", data=data)


@rights_violations_bp.route('/rights_violations/<int:rights_violation_id>/delete')
@login_required
def delete_rights_violation(rights_violation_id):
    rights_violation = session.query(RightsViolation).get(rights_violation_id)
    session.delete(rights_violation)
    session.commit()
    return redirect('/rights_violations/all?success=1')


@rights_violations_bp.route('/rights_violations/<int:rights_violation_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_rights_violation(rights_violation_id):
    rights_violation = session.query(RightsViolation).get(rights_violation_id)
    rights_violation_form = RightsViolationForm(request.form, obj=rights_violation)

    if helpers.validate_form_on_submit(rights_violation_form):
        rights_violation_form.populate_obj(rights_violation)
        return redirect('/rights_violations/{}?success=1'.format(rights_violation_id))

    data = copy(names)
    data['data'] = rights_violation

    return render_template("item_edit.html", data=data, form=rights_violation_form, action='edit')