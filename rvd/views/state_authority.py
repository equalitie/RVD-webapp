from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.StateAuthority import StateAuthorityForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, StateAuthority
from copy import copy
names = {
    'name': 'state authority',
    'plural': 'state authorities',
    'slug': 'state_authority',
    'plural_slug': 'state_authorities'
}
state_authority_bp = Blueprint('state_authority', __name__)


def get_name_from_id(needle, things):
    for thing in things:
        if int(thing.id) == int(needle):
            return thing


def gather_form_data():
    state_authority_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    state_authority_instance = StateAuthority(**state_authority_dict)
    session.add(state_authority_instance)
    session.commit()

    return state_authority_instance


@state_authority_bp.route('/state_authorities/add', methods=('GET', 'POST'))
@login_required
def state_authority():
    state_authority_form = StateAuthorityForm(request.form)
    if helpers.validate_form_on_submit(state_authority_form):
        state_authority_instance = gather_form_data()
        return redirect('/state_authorities/{}?success=1'.format(state_authority_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=state_authority_form, action='add', data=data)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    from sqlalchemy.inspection import inspect

    for r in inspect(StateAuthority).relationships:
        associated_data = getattr(obj, r.key)
        fields[r.key] = ", ".join([a.name for a in associated_data]) if associated_data else None
    return fields


@state_authority_bp.route('/state_authorities/<int:state_authority_id>')
@login_required
def view_state_authority(state_authority_id):
    state_authorities = session.query(StateAuthority).get(state_authority_id)
    fields = flatten_instance(state_authorities)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@state_authority_bp.route('/state_authorities/all')
@login_required
def view_all_state_authority():
    all_state_authority = session.query(StateAuthority).all()
    all_state_authority = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_state_authority]
    data = copy(names)
    data['data'] = all_state_authority

    return render_template("item_view_all.html", data=data)


@state_authority_bp.route('/state_authorities/<int:state_authority_id>/delete')
@login_required
def delete_state_authority(state_authority_id):
    state_authorities = session.query(StateAuthority).get(state_authority_id)
    session.delete(state_authorities)
    session.commit()
    return redirect('/state_authorities/all?success=1')


@state_authority_bp.route('/state_authorities/<int:state_authority_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_state_authority(state_authority_id):
    state_authorities = session.query(StateAuthority).get(state_authority_id)
    state_authority_form = StateAuthorityForm(request.form, obj=state_authorities)

    if helpers.validate_form_on_submit(state_authority_form):
        state_authority_form.populate_obj(state_authorities)
        return redirect('/state_authorities/{}?success=1'.format(state_authority_id))

    data = copy(names)
    data['data'] = state_authorities

    return render_template("item_edit.html", data=data, form=state_authority_form, action='edit')