from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.ReleaseType import ReleaseTypeForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, ReleaseType
from copy import copy
from rvd.views import flatten_instance
names = {
    'name': 'release type',
    'plural': 'release types',
    'slug': 'release_type',
    'plural_slug': 'release_types'
}
release_types_bp = Blueprint('release_types', __name__)


def gather_form_data():
    release_type_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    release_type_instance = ReleaseType(**release_type_dict)
    session.add(release_type_instance)
    session.flush()

    return release_type_instance


@release_types_bp.route('/release_types/add', methods=('GET', 'POST'))
@login_required
def release_types():
    release_type_form = ReleaseTypeForm(request.form)
    if helpers.validate_form_on_submit(release_type_form):
        release_type_instance = gather_form_data()
        return redirect('/release_types/{}?success=1'.format(release_type_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=release_type_form, action='add', data=data)


@release_types_bp.route('/release_types/<int:release_type_id>')
@login_required
def view_release_type(release_type_id):
    release_type = session.query(ReleaseType).get(release_type_id)
    fields = flatten_instance(release_type, ReleaseType)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@release_types_bp.route('/release_types/all')
@login_required
def view_all_release_types():
    all_release_types = session.query(ReleaseType).all()
    all_release_types = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_release_types]
    data = copy(names)
    data['data'] = all_release_types

    return render_template("item_view_all.html", data=data)


@release_types_bp.route('/release_types/<int:release_type_id>/delete')
@login_required
def delete_release_type(release_type_id):
    release_type = session.query(ReleaseType).get(release_type_id)
    session.delete(release_type)
    session.flush()
    return redirect('/release_types/all?success=1')


@release_types_bp.route('/release_types/<int:release_type_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_release_type(release_type_id):
    release_type = session.query(ReleaseType).get(release_type_id)
    release_type_form = ReleaseTypeForm(request.form, obj=release_type)

    if helpers.validate_form_on_submit(release_type_form):
        release_type_form.populate_obj(release_type)
        return redirect('/release_types/{}?success=1'.format(release_type_id))

    data = copy(names)
    data['data'] = release_type

    return render_template("item_edit.html", data=data, form=release_type_form, action='edit')