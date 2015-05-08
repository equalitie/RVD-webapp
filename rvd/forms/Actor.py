from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models


class ActorForm(ModelForm):

    class Meta:
        model = models.Actor

    __order = (
        'name', 'birth_date', 'gender', 'telephone', 'address', 'is_activist',
        'activist_info', 'organisations', 'professions', 'locations'
    )

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    organisations = fields.SelectMultipleField(choices=[
        ('0', "The Guardian"), ('1', "Propublica"), ('2', "The Intercept"), ('3', "The Washington Post")])
    professions = fields.SelectMultipleField(choices=[
        ('0', "Programmer"), ('1', "Journalist"), ('2', "Writer"), ('3', "Wizard")])
    locations = fields.SelectMultipleField(choices=[
        ('0', "Montreal, QC"), ('1', "Toronto, ON"), ('2', "San Francisco, CA"), ('3', "Vancouver, BC")])
    gender = fields.SelectField(___('Gender'), validators=[validators.required()], choices=[
        ('M', ___('Male')), ('F', ___('Female'))])
    is_activist = fields.SelectField(___('Is activist'), validators=[validators.required()], choices=[
        (1, ___('Yes')), (0, ___('No'))], coerce=bool)
