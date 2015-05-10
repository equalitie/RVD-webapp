from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Location import LocationForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session
from rvd.models import Location
from copy import copy
names = {
    'name': 'location',
    'plural': 'locations',
    'slug': 'location',
    'plural_slug': 'locations'
}
locations_bp = Blueprint('locations', __name__)


def gather_form_data():
    location_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    location_instance = Location(**location_dict)
    session.add(location_instance)
    session.commit()

    return location_instance


@locations_bp.route('/locations/add', methods=('GET', 'POST'))
@login_required
def locations():
    location_form = LocationForm(request.form)
    if helpers.validate_form_on_submit(location_form):
        location_instance = gather_form_data()
        return redirect('/locations/{}?success=1'.format(location_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=location_form, action='add', data=data)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    from sqlalchemy.inspection import inspect

    for r in inspect(Location).relationships:
        associated_data = getattr(obj, r.key)
        fields[r.key] = ", ".join([a.name for a in associated_data]) if associated_data else None
    return fields


@locations_bp.route('/locations/<int:location_id>')
@login_required
def view_location(location_id):
    location = session.query(Location).get(location_id)
    fields = flatten_instance(location)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@locations_bp.route('/locations/all')
@login_required
def view_all_locations():
    all_locations = session.query(Location).all()
    all_locations = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_locations]
    data = copy(names)
    data['data'] = all_locations

    return render_template("item_view_all.html", data=data)


@locations_bp.route('/locations/<int:location_id>/delete')
@login_required
def delete_location(location_id):
    location = session.query(Location).get(location_id)
    session.delete(location)
    session.commit()
    return redirect('/locations/all?success=1')


@locations_bp.route('/locations/<int:location_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_location(location_id):
    location = session.query(Location).get(location_id)
    location_form = LocationForm(request.form, obj=location)

    if helpers.validate_form_on_submit(location_form):
        location_form.populate_obj(location)
        return redirect('/locations/{}?success=1'.format(location_id))

    data = copy(names)
    data['data'] = location

    return render_template("item_edit.html", data=data, form=location_form, action='edit')