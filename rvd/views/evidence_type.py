from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.EvidenceType import EvidenceTypeForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, EvidenceType
from rvd.forms import event_factory
from copy import copy
from rvd.views import get_name_from_id, flatten_instance
names = {
    'name': 'evidence_type',
    'plural': 'evidence_types',
    'slug': 'evidence_type',
    'plural_slug': 'evidence_types'
}
evidence_types_bp = Blueprint('evidence_types', __name__)


def gather_form_data():
    evidence_type_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

    event = request.form.getlist('event')
    evs = event_factory()
    evidence_type_dict['event'] = get_name_from_id(event[0], evs)

    evidence_type_instance = EvidenceType(**evidence_type_dict)
    session.add(evidence_type_instance)
    session.commit()

    return evidence_type_instance


@evidence_types_bp.route('/evidence_types/add', methods=('GET', 'POST'))
@login_required
def evidence_types():
    evidence_type_form = EvidenceTypeForm(request.form)
    if helpers.validate_form_on_submit(evidence_type_form):
        evidence_type_instance = gather_form_data()
        return redirect('/evidence_types/{}?success=1'.format(evidence_type_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=evidence_type_form, action='add', data=data)


@evidence_types_bp.route('/evidence_types/<int:evidence_type_id>')
@login_required
def view_evidence_type(evidence_type_id):
    evidence_type = session.query(EvidenceType).get(evidence_type_id)
    fields = flatten_instance(evidence_type, EvidenceType)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@evidence_types_bp.route('/evidence_types/all')
@login_required
def view_all_evidence_types():
    all_evidence_types = session.query(EvidenceType).all()
    all_evidence_types = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_evidence_types]
    data = copy(names)
    data['data'] = all_evidence_types

    return render_template("item_view_all.html", data=data)


@evidence_types_bp.route('/evidence_types/<int:evidence_type_id>/delete')
@login_required
def delete_evidence_type(evidence_type_id):
    evidence_type = session.query(EvidenceType).get(evidence_type_id)
    session.delete(evidence_type)
    session.flush()
    return redirect('/evidence_types/all?success=1')


@evidence_types_bp.route('/evidence_types/<int:evidence_type_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_evidence_type(evidence_type_id):
    evidence_type = session.query(EvidenceType).get(evidence_type_id)
    evidence_type_form = EvidenceTypeForm(request.form, obj=evidence_type)

    if helpers.validate_form_on_submit(evidence_type_form):
        evidence_type_form.populate_obj(evidence_type)
        return redirect('/evidence_types/{}?success=1'.format(evidence_type_id))

    data = copy(names)
    data['data'] = evidence_type

    return render_template("item_edit.html", data=data, form=evidence_type_form, action='edit')