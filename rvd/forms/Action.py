from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class ActionForm(ModelForm):

    class Meta:
        model = models.Action
   
    # While the relationship from an action to (state/inter.) authorities is many to many,
    # the complaint_to_(state/inter.)_authority fields are just text blobs.
    # It might thus make sense to request that multiple complaints be entered in one field
    # and be separated by a blank line.
    __order = (
        'state_bodies_approached', 'complaint_to_state_authority', 'response_from_state_authority',
        'international_bodies_approached', 'complaint_to_international_authority',
        'response_from_international_authority', 'events'
    )

    def __iter__(self):
        f = list(super(ModelForm, self).__init__())
        gf = lambda fid: next((fld for fld in f if fld.id == fid))
        return (gf(fid) for fid in self.__order)
    
    state_bodies_approached = fields.SelectMultipleField(choices=[
        (str(i), s) for i, s in enumerate(['The Sheriff', 'Head of Police', 'Minister'])])
    international_bodies_approached = fields.SelectMultipleField(choices=[
        (str(i), n) for i, n in enumerate(['United Nations', 'Amnesty International'])])
    events = fields.SelectMultipleField(choices=[
        (str(i), e) for i, e in enumerate(['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5'])])
