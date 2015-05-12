from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Event import EventForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, Event
from flask_login import current_user
from rvd.forms import location_factory, prison_factory, release_type_factory, source_factory, witnesses_factory
from rvd.forms import perpetrators_factory, victims_factory
from sqlalchemy import and_
from copy import copy
from sqlalchemy.orm.exc import NoResultFound
names = {
    'name': 'event',
    'plural': 'events',
    'slug': 'event',
    'plural_slug': 'events'
}
events_bp = Blueprint('events', __name__)


def get_name_from_id(needle, things):
    for thing in things:
        if int(thing.id) == int(needle):
            return thing


def gather_form_data():
    event_dict = defaultdict(lambda: None, {value: field if field else None for value, field in request.form.iteritems()})

    location_ids = request.form.getlist('locations')
    event_dict['locations'] = [get_name_from_id(x, location_factory()) for x in location_ids]

    prison_ids = request.form.getlist('prisons')
    event_dict['prisons'] = [get_name_from_id(x, prison_factory()) for x in prison_ids]

    release_types_ids = request.form.getlist('release_types')
    event_dict['release_types'] = [get_name_from_id(x, release_type_factory()) for x in release_types_ids]

    sources_ids = request.form.getlist('sources')
    event_dict['sources'] = [get_name_from_id(x, source_factory()) for x in sources_ids]

    witnesses_ids = request.form.getlist('witnesses')
    event_dict['witnesses'] = [get_name_from_id(x, witnesses_factory()) for x in witnesses_ids]

    victims_ids = request.form.getlist('victims')
    event_dict['victims'] = [get_name_from_id(x, victims_factory()) for x in victims_ids]

    perpetrators_ids = request.form.getlist('perpetrators')
    event_dict['perpetrators'] = [get_name_from_id(x, perpetrators_factory()) for x in perpetrators_ids]

    event_dict['owner_id'] = current_user.id

    event_instance = Event(**event_dict)
    session.add(event_instance)
    session.commit()

    return event_instance


@events_bp.route('/events/add', methods=('GET', 'POST'))
@login_required
def events():
    event_form = EventForm(request.form)
    if helpers.validate_form_on_submit(event_form):
        event_instance = gather_form_data()
        return redirect('/events/{}?success=1'.format(event_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=event_form, action='add', data=data)


def get_attr(a):
    if hasattr(a, 'name'):
        return a.name
    if hasattr(a, 'type_code'):
        return str(a.type_code)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    from sqlalchemy.inspection import inspect

    for r in inspect(Event).relationships:
        associated_data = getattr(obj, r.key)
        try:
            fields[r.key] = ", ".join([get_attr(a) for a in associated_data]) if associated_data else None
        except TypeError:
            fields[r.key] = associated_data.email
    return fields


@events_bp.route('/events/<int:event_id>')
@login_required
def view_event(event_id):
    data = copy(names)
    try:
        if current_user.is_admin:
            event = session.query(Event).get(event_id)
        else:
            event = session.query(Event).filter(and_(Event.id == event_id, Event.owner_id == current_user.id)).one()
        fields = flatten_instance(event)
    except NoResultFound:
        return redirect('/events/all')
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@events_bp.route('/events/all')
@login_required
def view_all_events():
    if current_user.is_admin:
        all_events = session.query(Event).all()
    else:
        all_events = session.query(Event).filter(Event.owner_id == current_user.id)
    all_events = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_events]
    data = copy(names)
    data['data'] = all_events

    return render_template("item_view_all.html", data=data)


@events_bp.route('/events/<int:event_id>/delete')
@login_required
def delete_event(event_id):
    try:
        if current_user.is_admin:
            event = session.query(Event).get(event_id)
        else:
            event = session.query(Event).filter(and_(Event.id == event_id, Event.owner_id == current_user.id)).one()
    except NoResultFound:
        return redirect('/events/all')
    session.delete(event)
    session.commit()
    return redirect('/events/all?success=1')


@events_bp.route('/events/<int:event_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_event(event_id):
    try:
        if current_user.is_admin:
            event = session.query(Event).get(event_id)
        else:
            event = session.query(Event).filter(and_(Event.id == event_id, Event.owner_id == current_user.id)).one()
    except NoResultFound:
        return redirect('/events/all')

    event_form = EventForm(request.form, obj=event)

    if helpers.validate_form_on_submit(event_form):
        event_form.populate_obj(event)
        return redirect('/events/{}?success=1'.format(event_id))

    data = copy(names)
    data['data'] = event

    return render_template("item_edit.html", data=data, form=event_form, action='edit')