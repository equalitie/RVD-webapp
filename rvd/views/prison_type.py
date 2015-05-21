from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.PrisonType import PrisonTypeForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session
from rvd.models import PrisonType
from copy import copy
from rvd.views import flatten_instance
names = {
    'name': 'prison type',
    'plural': 'prison types',
    'slug': 'prison_type',
    'plural_slug': 'prison_types'
}
prison_types_bp = Blueprint('prison_types', __name__)


def gather_form_data():
    prison_type_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    prison_type_instance = PrisonType(**prison_type_dict)
    session.add(prison_type_instance)
    session.commit()

    return prison_type_instance


@prison_types_bp.route('/prison_types/add', methods=('GET', 'POST'))
@login_required
def prison_types():
    prison_type_form = PrisonTypeForm(request.form)
    if helpers.validate_form_on_submit(prison_type_form):
        prison_type_instance = gather_form_data()
        return redirect('/prison_types/{}?success=1'.format(prison_type_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=prison_type_form, action='add', data=data)


@prison_types_bp.route('/prison_types/<int:prison_type_id>')
@login_required
def view_prison_type(prison_type_id):
    prison_type = session.query(PrisonType).get(prison_type_id)
    fields = flatten_instance(prison_type, PrisonType)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@prison_types_bp.route('/prison_types/all')
@login_required
def view_all_prison_types():
    all_prison_types = session.query(PrisonType).all()
    all_prison_types = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_prison_types]
    data = copy(names)
    data['data'] = all_prison_types

    return render_template("item_view_all.html", data=data)


@prison_types_bp.route('/prison_types/<int:prison_type_id>/delete')
@login_required
def delete_prison_type(prison_type_id):
    prison_type = session.query(PrisonType).get(prison_type_id)
    session.delete(prison_type)
    session.flush()
    return redirect('/prison_types/all?success=1')


@prison_types_bp.route('/prison_types/<int:prison_type_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_prison_type(prison_type_id):
    prison_type = session.query(PrisonType).get(prison_type_id)
    prison_type_form = PrisonTypeForm(request.form, obj=prison_type)

    if helpers.validate_form_on_submit(prison_type_form):
        prison_type_form.populate_obj(prison_type)
        return redirect('/prison_types/{}?success=1'.format(prison_type_id))

    data = copy(names)
    data['data'] = prison_type

    return render_template("item_edit.html", data=data, form=prison_type_form, action='edit')