from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.User import UserForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, User
from rvd.forms import user_org_factory
from copy import copy
names = {
    'name': 'user',
    'plural': 'users',
    'slug': 'user',
    'plural_slug': 'users'
}
users_bp = Blueprint('users', __name__)


def get_name_from_id(needle, things):
    for thing in things:
        if int(thing.id) == int(needle):
            return thing


def gather_form_data():
    user_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

    organisation = request.form.getlist('organisation')
    if organisation:
        orgs = user_org_factory()
        user_dict['organisation'] = get_name_from_id(organisation[0], orgs)
    else:
        user_dict['organisation'] = None

    user_instance = User(**user_dict)
    session.add(user_instance)
    session.commit()

    return user_instance


@users_bp.route('/users/add', methods=('GET', 'POST'))
@login_required
def users():
    user_form = UserForm(request.form)
    if helpers.validate_form_on_submit(user_form):
        user_instance = gather_form_data()
        return redirect('/users/{}?success=1'.format(user_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=user_form, action='add', data=data)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    from sqlalchemy.inspection import inspect

    for r in inspect(User).relationships:
        associated_data = getattr(obj, r.key)
        try:
            fields[r.key] = ", ".join([a.title for a in associated_data]) if associated_data else None
        except TypeError:
            fields[r.key] = associated_data.name
    return fields


@users_bp.route('/users/<int:user_id>')
@login_required
def view_user(user_id):
    user = session.query(User).get(user_id)
    fields = flatten_instance(user)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@users_bp.route('/users/all')
@login_required
def view_all_users():
    all_users = session.query(User).all()
    all_users = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_users]
    data = copy(names)
    data['data'] = all_users

    return render_template("item_view_all.html", data=data)


@users_bp.route('/users/<int:user_id>/delete')
@login_required
def delete_user(user_id):
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    return redirect('/users/all?success=1')


@users_bp.route('/users/<int:user_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_user(user_id):
    user = session.query(User).get(user_id)
    user_form = UserForm(request.form, obj=user)

    if helpers.validate_form_on_submit(user_form):
        user_form.populate_obj(user)
        return redirect('/users/{}?success=1'.format(user_id))

    data = copy(names)
    data['data'] = user

    return render_template("item_edit.html", data=data, form=user_form, action='edit')