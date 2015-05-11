from flask_babel import lazy_gettext as ___
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import validators
from wtforms_alchemy import ModelForm
from rvd.forms import user_org_factory
from rvd.models import User
from wtforms.fields import PasswordField, SelectField
from wtforms_components import EmailField


class UserForm(ModelForm):

    class Meta:
        model = User

    __order = ('email', 'password', 'organisation', 'is_admin')

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    email = EmailField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])
    organisation = QuerySelectField(query_factory=user_org_factory, get_label='name', allow_blank=True)
    is_admin = SelectField(
        ___('Is admin'), validators=[validators.required()], choices=[(1, ___('Yes')), (0, ___('No'))], coerce=bool
    )


