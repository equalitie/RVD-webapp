from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class EventForm(ModelForm):
    
    class Meta:
        model = models.Event
    
    __order = (
        'title', 'description', 'detention_date', 'release_date', 'report_date',
        'charges', 'consequences', 'psych_assist', 'material_assist', 'was_activist',
        'victim_is_complainant', 'allow_storage', 'allow_publishing', 'allow_representation',
        'data_is_sensitive', 'locations', 'prisons', 'release_types', 'sources',
        'witnesses', 'victims', 'perpetrators'
    )

    def __iter__(self):
        f = list(super(ModelForm, self).__init__())
        gf = lambda fid: next((fld for fld in f if fld.id == fid))
        return (gf(fid) for fid in self.__order)
   
    # Use some example data for populating the form before we have some data to work with
    release_types = fields.SelectMultipleField(choices=[
        (str(i), t) for i, t in enumerate(['type1', 'type2', 'type3'])])
    locations = fields.SelectMultipleField(choices=[
        (str(i), l) for i, l in enumerate(['California', 'Ontario', 'Montreal', 'Washington'])])
    prisons = fields.SelectMultipleField(choices=[
        (str(i), p) for i, p in enumerate(['Guantanamo', 'Bordeaux'])])
    sources = fields.SelectMultipleField(choices=[
        (str(i), s) for i, s in enumerate(['John Smith', 'Jane Doe', 'Bob Grant', 'Alice McDonald'])])
    witnesses = fields.SelectMultipleField(choices=[
        (str(i), w) for i, w in enumerate(['Jane Grace', 'Flander Flowers', 'Sarah Noble'])])
    victims = fields.SelectMultipleField(choices=[
        (str(i), v) for i, v in enumerate(['Greg Housh', 'Jeremy Hammond', 'Barret Brown'])])
    perpetrators = fields.SelectMultipleField(choices=[
        (str(i), p) for i, p in enumerate(['NYC Police', 'Obama', 'Bush'])])
