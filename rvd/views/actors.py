from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Actor import ActorForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session
import datetime

actors_bp = Blueprint('actors', __name__)

from rvd.models import Actor, Organisation, Location, Profession


def gather_form_data(actor_form, new_actor=True, current_actor=None):
    actor_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

    organisations = request.form.getlist('organisations')
    test_org_loc = [Location(name='Test Location', longitude=44.0123, latitude=23.235)]
    organisations = [
        Organisation(name=actor_form.organisations.choices[i][1], description='test', locations=test_org_loc)
        for i in map(int, organisations)]
    actor_dict['organisations'] = organisations
    locations = request.form.getlist('locations')
    locations = [
        Location(name=actor_form.locations.choices[i][1], latitude=41.123, longitude=67.15)
        for i in map(int, locations)]
    actor_dict['locations'] = locations
    professions = request.form.getlist('professions')
    professions = [Profession(name=actor_form.professions.choices[i][1]) for i in map(int, professions)]
    actor_dict['professions'] = professions

    actor_dict['gender'] = actor_dict['gender']
    actor_dict['is_activist'] = actor_dict['is_activist']
    actor_dict['birth_date'] = datetime.datetime.strptime(actor_dict['birth_date'], "%Y-%m-%d").date()

    actor_instance = Actor(**actor_dict)
    if new_actor:
        session.add(actor_instance)

    session.commit()

    return actor_instance


@actors_bp.route('/actors/add', methods=('GET', 'POST'))
@login_required
def actors():
    actor_form = ActorForm(request.form)
    if helpers.validate_form_on_submit(actor_form):
        actor_instance = gather_form_data(actor_form)
        return redirect('/actors/{}?success=1'.format(actor_instance.id))

    return render_template("actor_edit.html", form=actor_form, action='add')


@actors_bp.route('/actors/<int:actor_id>')
@login_required
def view_actor(actor_id):
    actor = session.query(Actor).get(actor_id)
    actor = {k: v for k, v in actor.__dict__.iteritems() if k != "_sa_instance_state"}

    return render_template("actor_view.html", actor=actor)


@actors_bp.route('/actors/all')
@login_required
def view_all_actors():
    all_actors = session.query(Actor).all()
    all_actors = [{k: v for k, v in x.__dict__.iteritems() if k != "_sa_instance_state"} for x in all_actors]

    return render_template("actors_view_all.html", actors=all_actors)


@actors_bp.route('/actors/<int:actor_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_actor(actor_id):
    actor = session.query(Actor).get(actor_id)
    actor_form = ActorForm(request.form, obj=actor)

    if helpers.validate_form_on_submit(actor_form):
        gather_form_data(actor_form, new_actor=False, current_actor=actor)
        return redirect('/actors/{}?success=1'.format(actor_id))

    return render_template("actor_edit.html", actor=actor, form=actor_form, action='edit')