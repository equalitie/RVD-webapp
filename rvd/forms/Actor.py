from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class ActorForm(ModelForm):

    class Meta:
        model = models.Actor

    # this is a bit shitty, but required if we want to have a proper order in the fields.
    # if you move/change fields, they HAVE to be added here, until this code is made better...
    __order = (
        'name', 'birth_date', 'gender', 'telephone', 'address', 'is_activist',
        'activist_info', 'organisations', 'professions', 'locations'
    )

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    # because some of the sqlalchemy types don't map so well to these types (some are relationships),
    # these are overrides.
    organisations = fields.SelectMultipleField(choices=[
        ('0', "The Guardian"), ('1', "Propublica"), ('2', "The Intercept"), ('3', "The Washington Post")])
    professions = fields.SelectMultipleField(choices=[
        ('0', "Programmer"), ('1', "Journalist"), ('2', "Writer"), ('3', "Wizard")])
    locations = fields.SelectMultipleField(choices=[
        ('0', "Montreal, QC"), ('1', "Toronto, ON"), ('2', "San Francisco, CA"), ('3', "Vancouver, BC")])
    gender = fields.RadioField(___('Gender'), validators=[validators.required()], choices=[
        ('True', ___('Male')), ('False', ___('Female'))])
    is_activist = fields.RadioField(___('Is activist'), validators=[validators.required()], choices=[
        ('True', ___('Yes')), ('False', ___('No'))])
