from flask import Blueprint, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename 
from flask_login import login_required
from rvd.forms.Event import EventForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, Event, EventType, Location, User, Document
from rvd.views import flatten_instance, get_name_from_id
from flask_login import current_user
from rvd.forms import location_factory, prison_factory, release_type_factory, source_factory, witnesses_factory
from rvd.forms import perpetrators_factory, victims_factory, event_type_factory
from sqlalchemy import and_
from copy import copy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect
from itertools import groupby
import datetime
import os
names = {
    'name': 'event',
    'plural': 'events',
    'slug': 'event',
    'plural_slug': 'events'
}
events_bp = Blueprint('events', __name__)
DOC_FOLDER = 'lib/static/documents'

def gather_form_data():

    event_dict = defaultdict(lambda: None, {value: field if field else None for value, field in request.form.iteritems()})
    
    uploaded_docs = request.files.getlist("documents")
    documents_to_save = []
    event_dict['documents'] = []
    if uploaded_docs:
        for file in uploaded_docs:
            filename = secure_filename(file.filename)
            file.save(os.path.join(DOC_FOLDER, filename))
            doc = Document()
            doc.filename = filename
            session.add(doc)
            session.commit()
            event_dict['documents'].append(doc)

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

    event_types = request.form.getlist('event_types')
    event_dict['event_types'] = [get_name_from_id(x, event_type_factory()) for x in event_types]


    event_dict['owner_id'] = current_user.id
    event_instance = Event(**event_dict)
    session.add(event_instance)
    session.flush()

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


def get_event_violations_type(obj):
    fields = {'id': obj.id}
    for r in inspect(Event).relationships:
        if r.key == "event_types":
            associated_data = getattr(obj, r.key)
            fields['event_types'] = [a.id for a in associated_data]
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
        fields = flatten_instance(event, Event)
    except NoResultFound:
        return redirect('/events/all')
    data['data'] = fields

    return render_template("item_view_single.html", data=data, event=event.__dict__)


@events_bp.route('/events/grouped')
@login_required
def events_by_type():
    event_types = request.args.get("event_types", None)
    event_types_list = event_types.split(",")

    locations = request.args.get("locations", None)
    locations_list = locations.split(",")

    violations_start_date = request.args.get("start_date", None)
    violations_end_date = request.args.get("end_date", None)

    violations_start_date = datetime.datetime.fromtimestamp(float(violations_start_date)).strftime('%Y-%m-%d')
    violations_end_date = datetime.datetime.fromtimestamp(float(violations_end_date)).strftime('%Y-%m-%d')

    event_types = [x for x in event_type_factory()]
    event_type_names = [{"id": x.id, "name": x.name} for x in event_types]

    ands = [EventType.id.in_(event_types_list), Event.report_date >= violations_start_date,
            Event.report_date <= violations_end_date, Location.id.in_(locations_list)]

    # add extra restriction about user/owner if logged in user is not an admin
    if not current_user.is_admin:
        ands.append(User.organisation_id == current_user.organisation_id)

    all_events = session.query(
        Event
    ).join(
        Event.event_type
    ).join(
        Event.locations
    ).join(
        Event.owner
    ).filter(
        and_(x for x in ands)
    )

    grouped_events = []
    locations = []

    for event in all_events:
        event_locations = event.locations
        for location in event_locations:
            locations.append([getattr(location, 'latitude'), getattr(location, 'longitude')])

    # group by date first
    all_events = sorted(all_events, key=lambda z: z.report_date)
    for date, group in groupby(all_events, key=lambda y: y.report_date):
        # group by type, make sure we have a default of 0
        date_types = {"{}".format(x.id): 0 for x in event_types}
        date_types["date"] = date.strftime("%Y%m%d")
        event_objs = [get_event_violations_type(e) for e in list(group)]
        for violation in event_objs:
            if violation['event_types']:
                for v in violation['event_types']:
                    label = "{}".format(v)
                    date_types[label] += 1
        grouped_events.append(date_types)

    return jsonify({"events": grouped_events, "locations": locations, "names": event_type_names})


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
    session.flush()
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
