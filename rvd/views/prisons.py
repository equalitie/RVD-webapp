from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Prison import PrisonForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, Prison
from rvd.forms import location_factory, prison_type_factory
from copy import copy
from rvd.views import flatten_instance, get_name_from_id
names = {
    'name': 'prison',
    'plural': 'prisons',
    'slug': 'prison',
    'plural_slug': 'prisons'
}
prisons_bp = Blueprint('prisons', __name__)


def gather_form_data():
    prison_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

    locations = request.form.getlist('locations')
    locs = location_factory()
    prison_dict['locations'] = [get_name_from_id(x, locs) for x in locations]

    prison_types = request.form.getlist('prison_types')
    pt = prison_type_factory()
    prison_dict['prison_types'] = [get_name_from_id(x, pt) for x in prison_types]

    prison_instance = Prison(**prison_dict)
    session.add(prison_instance)
    session.flush()

    return prison_instance


@prisons_bp.route('/prisons/add', methods=('GET', 'POST'))
@login_required
def prisons():
    prison_form = PrisonForm(request.form)
    if helpers.validate_form_on_submit(prison_form):
        prison_instance = gather_form_data()
        return redirect('/prisons/{}?success=1'.format(prison_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=prison_form, action='add', data=data)


@prisons_bp.route('/prisons/<int:prison_id>')
@login_required
def view_prison(prison_id):
    prison = session.query(Prison).get(prison_id)
    fields = flatten_instance(prison, Prison)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@prisons_bp.route('/prisons/all')
@login_required
def view_all_prisons():
    all_prisons = session.query(Prison).all()
    all_prisons = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_prisons]
    data = copy(names)
    data['data'] = all_prisons

    return render_template("item_view_all.html", data=data)


@prisons_bp.route('/prisons/<int:prison_id>/delete')
@login_required
def delete_prison(prison_id):
    prison = session.query(Prison).get(prison_id)
    session.delete(prison)
    session.flush()
    return redirect('/prisons/all?success=1')


@prisons_bp.route('/prisons/<int:prison_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_prison(prison_id):
    prison = session.query(Prison).get(prison_id)
    prison_form = PrisonForm(request.form, obj=prison)

    if helpers.validate_form_on_submit(prison_form):
        prison_form.populate_obj(prison)
        return redirect('/prisons/{}?success=1'.format(prison_id))

    data = copy(names)
    data['data'] = prison

    return render_template("item_edit.html", data=data, form=prison_form, action='edit')