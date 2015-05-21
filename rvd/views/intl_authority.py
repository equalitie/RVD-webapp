from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.InternationalAuthority import InternationalAuthorityForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, InternationalAuthority
from rvd.views import flatten_instance
from copy import copy
names = {
    'name': 'international authority',
    'plural': 'international authorities',
    'slug': 'international_authority',
    'plural_slug': 'international_authorities'
}
international_authority_bp = Blueprint('international_authority', __name__)


def gather_form_data():
    international_authority_dict = defaultdict(
        lambda: None, {value: field for value, field in request.form.iteritems()}
    )
    international_authority_instance = InternationalAuthority(**international_authority_dict)
    session.add(international_authority_instance)
    session.flush()

    return international_authority_instance


@international_authority_bp.route('/international_authorities/add', methods=('GET', 'POST'))
@login_required
def international_authority():
    international_authority_form = InternationalAuthorityForm(request.form)
    if helpers.validate_form_on_submit(international_authority_form):
        international_authority_instance = gather_form_data()
        return redirect('/international_authorities/{}?success=1'.format(international_authority_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=international_authority_form, action='add', data=data)


@international_authority_bp.route('/international_authorities/<int:international_authority_id>')
@login_required
def view_international_authority(international_authority_id):
    intl_auth = session.query(InternationalAuthority).get(international_authority_id)
    fields = flatten_instance(intl_auth, InternationalAuthority)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@international_authority_bp.route('/international_authorities/all')
@login_required
def view_all_international_authority():
    all_international_authority = session.query(InternationalAuthority).all()
    all_international_authority = [
        {k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_international_authority
    ]

    data = copy(names)
    data['data'] = all_international_authority

    return render_template("item_view_all.html", data=data)


@international_authority_bp.route('/international_authorities/<int:international_authority_id>/delete')
@login_required
def delete_international_authority(international_authority_id):
    intl_auth = session.query(InternationalAuthority).get(international_authority_id)
    session.delete(intl_auth)
    session.flush()
    return redirect('/international_authorities/all?success=1')


@international_authority_bp.route(
    '/international_authorities/<int:international_authority_id>/edit', methods=('GET', 'POST')
)
@login_required
def edit_international_authority(international_authority_id):
    intl_auth = session.query(InternationalAuthority).get(international_authority_id)
    international_authority_form = InternationalAuthorityForm(request.form, obj=intl_auth)

    if helpers.validate_form_on_submit(international_authority_form):
        international_authority_form.populate_obj(intl_auth)
        return redirect('/international_authorities/{}?success=1'.format(international_authority_id))

    data = copy(names)
    data['data'] = intl_auth

    return render_template("item_edit.html", data=data, form=international_authority_form, action='edit')