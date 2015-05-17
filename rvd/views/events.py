from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required
from rvd.forms.Event import EventForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, Event, Action, RightsViolation, Location
from flask_login import current_user
from rvd.forms import location_factory, prison_factory, release_type_factory, source_factory, witnesses_factory
from rvd.forms import perpetrators_factory, victims_factory, rights_violations_factory
from sqlalchemy import and_
from copy import copy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect
from itertools import groupby
import datetime
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

    rights_violations = request.form.getlist('rights_violations')
    event_dict['rights_violations'] = [get_name_from_id(x, rights_violations_factory()) for x in rights_violations]

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
    if isinstance(a, Action):
        items = [u"{}: {}".format(k, v) for k, v in a.__dict__.iteritems() if k[0:4] != '_sa_']
        return ", ".join(items)
    if hasattr(a, 'name'):
        return a.name
    if hasattr(a, 'type_code'):
        return str(a.type_code)
    if hasattr(a, 'id'):
        return str(a.id)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)

    for r in inspect(Event).relationships:
        associated_data = getattr(obj, r.key)
        try:
            fields[r.key] = ", ".join([get_attr(a) for a in associated_data]) if associated_data else None
        except TypeError:
            fields[r.key] = associated_data.email
    return fields


def get_event_violations_type(obj):
    fields = {'id': obj.id}
    for r in inspect(Event).relationships:
        if r.key == "rights_violations":
            associated_data = getattr(obj, r.key)
            fields['rights_violations'] = [a.id for a in associated_data]
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


@events_bp.route('/events/grouped')
@login_required
def events_by_type():
    violation_types = request.args.get("violation_types", None)
    violation_types_list = violation_types.split(",")

    locations = request.args.get("locations", None)
    locations_list = locations.split(",")

    violations_start_date = request.args.get("start_date", None)
    violations_end_date = request.args.get("end_date", None)

    violations_start_date = datetime.datetime.fromtimestamp(float(violations_start_date)).strftime('%Y-%m-%d')
    violations_end_date = datetime.datetime.fromtimestamp(float(violations_end_date)).strftime('%Y-%m-%d')

    rights_violations_types = [x for x in rights_violations_factory()]
    rights_violations_names = [{"id": x.id, "name": x.name} for x in rights_violations_types]

    ands = [RightsViolation.id.in_(violation_types_list), Event.report_date >= violations_start_date,
            Event.report_date <= violations_end_date, Location.id.in_(locations_list)]

    # add extra restriction about user/owner if logged in user is not an admin
    if not current_user.is_admin:
        ands.append(Event.owner_id == current_user.id)

    all_events = session.query(Event).join(
        Event.rights_violations
    ).join(Event.locations).filter(and_(x for x in ands))

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
        date_types = {"{}".format(x.id): 0 for x in rights_violations_types}
        date_types["date"] = date.strftime("%Y%m%d")
        event_objs = [get_event_violations_type(e) for e in list(group)]
        for violation in event_objs:
            if violation['rights_violations']:
                for v in violation['rights_violations']:
                    label = "{}".format(v)
                    date_types[label] += 1
        grouped_events.append(date_types)

    return jsonify({"events": grouped_events, "locations": locations, "names": rights_violations_names})


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


# TODO DELETE ME!

@events_bp.route('/generate_data')
@login_required
def nasty_data_generator():
    from random import choice
    from datetime import timedelta
    from random import randint

    end = datetime.datetime.now()
    start = end - timedelta(days=30)


    items = [{
        "title": "an automated title",
        "description": "an automated desc",
        "detention_date": "2015-01-01",
        "release_date": "2015-01-02",
        "report_date": start + timedelta(seconds=randint(0, int((end - start).total_seconds()))),
        "locations": [choice(location_factory())],
        "prisons": [choice(prison_factory())],
        "release_types": [choice(release_type_factory())],
        "sources": [choice(source_factory())],
        "witnesses": [choice(witnesses_factory())],
        "victims": [choice(victims_factory())],
        "perpetrators": [choice(perpetrators_factory())],
        "rights_violations": [choice(rights_violations_factory())],
        "owner_id": current_user.id,
        "psych_assist": False,
        "material_assist": False,
        "was_activist": False,
        "victim_is_complainant": False,
        "allow_storage": False,
        "allow_publishing": False,
        "allow_representation": False,
        "data_is_sensitive": False,
        "public": False
    } for _ in xrange(100)]
    items = [Event(**x) for x in items]

    session.add_all(items)
    session.commit()

    return "1"