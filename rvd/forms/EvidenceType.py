from wtforms_alchemy import ModelForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from rvd.models import EvidenceType
from rvd.forms import event_factory


class EvidenceTypeForm(ModelForm):
    
    class Meta:
        model = EvidenceType
    
    __order = ('name', 'description', 'event')

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)
   
    event = QuerySelectField(query_factory=event_factory, get_label='title')

