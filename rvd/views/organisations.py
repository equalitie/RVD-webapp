from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Organisation import OrganisationForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session
from rvd.models import Organisation
from rvd.forms import location_factory
from copy import copy
names = {
    'name': 'organisation',
    'plural': 'organisations',
    'slug': 'organisation',
    'plural_slug': 'organisations'
}
organisations_bp = Blueprint('organisations', __name__)


def get_name_from_id(needle, things):
    for thing in things:
        if int(thing.id) == int(needle):
            return thing


def gather_form_data():
    organisation_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

    locations = request.form.getlist('locations')
    locs = location_factory()
    organisation_dict['locations'] = [get_name_from_id(x, locs) for x in locations]

    organisation_instance = Organisation(**organisation_dict)
    session.add(organisation_instance)
    session.commit()

    return organisation_instance


@organisations_bp.route('/organisations/add', methods=('GET', 'POST'))
@login_required
def organisations():
    organisation_form = OrganisationForm(request.form)
    if helpers.validate_form_on_submit(organisation_form):
        organisation_instance = gather_form_data()
        return redirect('/organisations/{}?success=1'.format(organisation_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=organisation_form, action='add', data=data)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    from sqlalchemy.inspection import inspect

    for r in inspect(Organisation).relationships:
        associated_data = getattr(obj, r.key)
        fields[r.key] = ", ".join([a.name for a in associated_data]) if associated_data else None
    return fields


@organisations_bp.route('/organisations/<int:organisation_id>')
@login_required
def view_organisation(organisation_id):
    organisation = session.query(Organisation).get(organisation_id)
    fields = flatten_instance(organisation)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@organisations_bp.route('/organisations/all')
@login_required
def view_all_organisations():
    all_organisations = session.query(Organisation).all()
    all_organisations = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_organisations]

    data = copy(names)
    data['data'] = all_organisations

    return render_template("item_view_all.html", data=data)


@organisations_bp.route('/organisations/<int:organisation_id>/delete')
@login_required
def delete_organisation(organisation_id):
    organisation = session.query(Organisation).get(organisation_id)
    session.delete(organisation)
    session.commit()
    return redirect('/organisations/all?success=1')


@organisations_bp.route('/organisations/<int:organisation_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_organisation(organisation_id):
    organisation = session.query(Organisation).get(organisation_id)
    organisation_form = OrganisationForm(request.form, obj=organisation)

    if helpers.validate_form_on_submit(organisation_form):
        organisation_form.populate_obj(organisation)
        return redirect('/organisations/{}?success=1'.format(organisation_id))

    data = copy(names)
    data['data'] = organisation

    return render_template("item_edit.html", data=data, form=organisation_form, action='edit')