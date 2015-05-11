from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import ModelForm
from rvd.forms import user_org_factory
from rvd.models import Organisation


class OrganisationForm(ModelForm):

    class Meta:
        model = Organisation

    __order = ('name', 'description', 'locations')

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    organisation = QuerySelectField(query_factory=user_org_factory, get_label='name')


