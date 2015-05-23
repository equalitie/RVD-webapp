from flask import Blueprint, render_template, request, redirect, abort
import json
from flask_login import login_required
from rvd.forms.Actor import ActorForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, Actor
import datetime
from flask_login import current_user
from rvd.forms import organisation_factory, location_factory, profession_factory
from copy import copy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from rvd.views import flatten_instance, get_name_from_id

names = {
    'name': 'actor',
    'plural': 'actors',
    'slug': 'actor',
    'plural_slug': 'actors'
}
actors_bp = Blueprint('actors', __name__)


def gather_form_data():
    actor_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    organisation_ids = request.form.getlist('organisations')
    actor_dict['organisations'] = [get_name_from_id(x, organisation_factory()) for x in organisation_ids]
    locations = request.form.getlist('locations')
    actor_dict['locations'] = [get_name_from_id(x, location_factory()) for x in locations]
    professions = request.form.getlist('professions')
    actor_dict['professions'] = [get_name_from_id(x, profession_factory()) for x in professions]
    actor_dict['gender'] = actor_dict['gender']
    actor_dict['is_activist'] = actor_dict['is_activist']
    actor_dict['birth_date'] = datetime.datetime.strptime(actor_dict['birth_date'], "%Y-%m-%d").date()
    actor_dict['owner_id'] = current_user.id

    actor_instance = Actor(**actor_dict)
    session.add(actor_instance)
    session.flush()

    return actor_instance


@actors_bp.route('/actors/add', methods=('GET', 'POST'))
@login_required
def actors():
    actor_form = ActorForm(request.form)
    if helpers.validate_form_on_submit(actor_form):
        actor_instance = gather_form_data()
        return redirect('/actors/{}?success=1'.format(actor_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=actor_form, action='add', data=data)


@actors_bp.route('/actors/<int:actor_id>')
@login_required
def view_actor(actor_id):
    data = copy(names)
    try:
        if current_user.is_admin:
            actor = session.query(Actor).get(actor_id)
        else:
            actor = session.query(Actor).filter(and_(Actor.id == actor_id, Actor.owner_id == current_user.id)).one()
        fields = flatten_instance(actor, Actor)
    except NoResultFound:
        return redirect('/actors/all')
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@actors_bp.route('/actors/all')
@login_required
def view_all_actors():
    if current_user.is_admin:
        all_actors = session.query(Actor).all()
    else:
        all_actors = session.query(Actor).filter(Actor.owner_id == current_user.id)
    all_actors = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_actors]
    data = copy(names)
    data['data'] = all_actors

    return render_template("item_view_all.html", data=data)


@actors_bp.route('/actors/<int:actor_id>/delete')
@login_required
def delete_actor(actor_id):
    try:
        if current_user.is_admin:
            actor = session.query(Actor).get(actor_id)
        else:
            actor = session.query(Actor).filter(and_(Actor.id == actor_id, Actor.owner_id == current_user.id)).one()
    except NoResultFound:
        return redirect('/actors/all')
    session.delete(actor)
    return redirect('/actors/all?success=1')


@actors_bp.route('/actors/<int:actor_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_actor(actor_id):
    try:
        if current_user.is_admin:
            actor = session.query(Actor).get(actor_id)
        else:
            actor = session.query(Actor).filter(and_(Actor.id == actor_id, Actor.owner_id == current_user.id)).one()
    except NoResultFound:
        return redirect('/actors/all')

    actor_form = ActorForm(request.form, obj=actor)

    if helpers.validate_form_on_submit(actor_form):
        actor_form.populate_obj(actor)
        return redirect('/actors/{}?success=1'.format(actor_id))

    data = copy(names)
    data['data'] = actor

    return render_template("item_edit.html", data=data, form=actor_form, action='edit')


@actors_bp.route('/search_witnesses')
@actors_bp.route('/search_victims')
@actors_bp.route('/search_perpetrators')
@login_required
def search_witnesses():
    term = request.args.get('term', None)
    if term is None:
        abort(401, "Missing term parameter")
    result = session.query(Actor).filter(Actor.name.like(("%{}%".format(term)))).all()
    return json.dumps([{"label": x.name, "value": x.id} for x in result])