from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class EvidenceTypeForm(ModelForm):
    
    class Meta:
        model = models.EvidenceType
    
    __order = ('name', 'description', 'event')

    def __iter__(self):
        f = list(super(ModelForm, self).__init__())
        gf = lambda fid: next((fld for fld in f if fld.id == fid))
        return (gf(fid) for fid in self.__order)
   
    # Use some example data for populating the form before we have some data to work with
    events = fields.SelectMultipleField(choices=[
        (str(i), e) for i, e in enumerate(['Event 1', 'Event 2', 'Event 3'])])
