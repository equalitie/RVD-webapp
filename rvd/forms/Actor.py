from flask_babel import lazy_gettext as ___
from wtforms_alchemy import ModelForm
from wtforms import fields, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from rvd.models import Actor
from rvd.forms import organisation_factory, location_factory, profession_factory


class ActorForm(ModelForm):

    class Meta:
        model = Actor

    __order = (
        'name', 'birth_date', 'gender', 'telephone', 'address', 'is_activist',
        'activist_info', 'organisations', 'professions', 'locations'
    )

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    organisations = QuerySelectMultipleField(query_factory=organisation_factory, get_label='name', allow_blank=True)
    professions = QuerySelectMultipleField(query_factory=profession_factory, get_label='name', allow_blank=True)
    locations = QuerySelectMultipleField(query_factory=location_factory, get_label='name', allow_blank=True)
    gender = fields.SelectField(___('Gender'), validators=[validators.required()], choices=[
        ('M', ___('Male')), ('F', ___('Female'))])
    is_activist = fields.SelectField(___('Is activist'), validators=[validators.required()], choices=[
        (1, ___('Yes')), (0, ___('No'))], coerce=bool)
