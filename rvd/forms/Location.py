from wtforms_alchemy import ModelForm
from rvd.models import Location


class LocationForm(ModelForm):

    class Meta:
        model = Location
