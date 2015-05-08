from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Event import EventForm 
from flask_admin import helpers
from rvd.models import session

events_bp = Blueprint('events', __name__)

from rvd.models import Event


def gather_form_data(event_form, new_event=True, current_event=None):
    pass


@events_bp.route('/events/add', methods=('GET', 'POST'))
@login_required
def events():
    event_form = EventForm(request.form)
    if helpers.validate_form_on_submit(event_form):
        event_instance = gather_form_data(event_form)
        return redirect('/events/{}'.format(event_instance.id))

    return render_template("event_edit.html", form=event_form, action='add')


@events_bp.route('/events/<int:event_id>')
@login_required
def view_event(event_id):
    event = session.query(Event).get(event_id)
    event = {k: v for k, v in event.__dict__.iteritems() if k != "_sa_instance_state"}

    return render_template("event_view.html", event=event)


@events_bp.route('/events/all')
@login_required
def view_all_events():
    all_events = session.query(Event).all()
    all_events = [{k: v for k, v in x.__dict__.iteritems() if k != "_sa_instance_state"} for x in all_events]

    return render_template("events_view_all.html", events=all_events)


@events_bp.route('/events/<int:event_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_event(event_id):
    event = session.query(Event).get(event_id)
    event_form = EventForm(request.form, obj=event)

    if helpers.validate_form_on_submit(event_form):
        gather_form_data(event_form, new_event=False, current_event=event)
        return redirect('/events/{}'.format(event_id))

    return render_template("event_edit.html", event=event, form=event_form, action='edit')