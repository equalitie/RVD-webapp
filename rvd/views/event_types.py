from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.EventTypes import EventTypesForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session
from rvd.models import EventType
from copy import copy
from rvd.views import flatten_instance
names = {
    'name': 'event type',
    'plural': 'event types',
    'slug': 'event_type',
    'plural_slug': 'event_types'
}
event_types_bp = Blueprint('event_types', __name__)


def gather_form_data():
    event_type_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    event_type_instance = EventType(**event_type_dict)
    session.add(event_type_instance)
    session.flush()

    return event_type_instance


@event_types_bp.route('/event_types/add', methods=('GET', 'POST'))
@login_required
def event_types():
    event_type_form = EventTypesForm(request.form)
    if helpers.validate_form_on_submit(event_type_form):
        event_type_instance = gather_form_data()
        return redirect('/event_types/{}?success=1'.format(event_type_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=event_type_form, action='add', data=data)


@event_types_bp.route('/event_types/<int:event_type_id>')
@login_required
def view_event_type(event_type_id):
    event_type = session.query(EventType).get(event_type_id)
    fields = flatten_instance(event_type, EventType)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@event_types_bp.route('/event_types/all')
@login_required
def view_all_event_types():
    all_event_types = session.query(EventType).all()
    all_event_types = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_event_types]

    data = copy(names)
    data['data'] = all_event_types

    return render_template("item_view_all.html", data=data)


@event_types_bp.route('/event_types/<int:event_type_id>/delete')
@login_required
def delete_event_type(event_type_id):
    event_type = session.query(EventType).get(event_type_id)
    session.delete(event_type)
    session.flush()
    return redirect('/event_types/all?success=1')


@event_types_bp.route('/event_types/<int:event_type_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_event_type(event_type_id):
    event_type = session.query(EventType).get(event_type_id)
    event_type_form = EventTypesForm(request.form, obj=event_type)

    if helpers.validate_form_on_submit(event_type_form):
        event_type_form.populate_obj(event_type)
        return redirect('/event_types/{}?success=1'.format(event_type_id))

    data = copy(names)
    data['data'] = event_type

    return render_template("item_edit.html", data=data, form=event_type_form, action='edit')